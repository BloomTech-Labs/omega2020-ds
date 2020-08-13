##################################################
## Omega2020 Flask App
##################################################
## MIT License
##################################################
## Authors: Labs 19 Team: Rob Hamilton, Johana Luna, Hira Khan, Rudy Enriquez
## Version: 1.0.0
##################################################

from flask import Flask, redirect, flash, request, render_template, jsonify
from .schema import DB, PuzzleTable, ModelTrainer
from decouple import config
from .pipeline import *
import boto3
import requests
import hashlib
import pandas as pd
import cv2
import json
#import scipy.misc
from PIL import Image
from io import BytesIO, StringIO
#from werkzeug.utils import secure_filename
import urllib.request
import sys
import logging
import re
from urllib.request import urlopen
import json
from tempfile import TemporaryFile
import psycopg2

from .ai import *
from .solver import *
from .dictionary import *


def create_app():
    """This is the core function with all of the Flask App Routes and logic that serves as the DS API. This first block of functions serves as adding core configuration settings such as FLASK, and Database configuration."""
    application = Flask(__name__)
    # CORS(application)
    application.debug = True
    application.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    application.config['ENV'] = config('FLASK_ENV')
    application.config['DEBUG'] = config('FLASK_DEBUG')
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    DB.init_app(application)
    model_path = config('MODEL_FILEPATH')

    """This is where AWS credentials are set globally for the App as well as what is the S3 bucket for use."""
    AWS = {
        'aws_access_key_id': config('S3_KEY'),
        'aws_secret_access_key': config('S3_SECRET')
    }
    ExtraArgs = json.loads(config('ExtraArgs'))
    s3 = boto3.client("s3", **AWS)

    S3_BUCKET = config('S3_BUCKET')
    S3_LOCATION = config('S3_LOCATION')

    def find_replace_multi(string, dictionary):
        """This function will take in a string, and remap values using a dictionary as the translator. The front end team indexes spaces on the Sudoku Board with two numbers from 0 to 8 representing columns and rows, whereas the Datascience team uses a Letter to represent the row and numbers to represent the column. So as the API outbounds information to the front end, coordinates are remapped for continuity of service."""
        for item in dictionary.keys():
            # sub item for item's paired value in string
            string = re.sub(item, dictionary[item], string)
        return string

    def upload_file_to_s3(*args):
        """This function takes the AWS arguments defined above, and will write a file to S3, and returns the S3 URL for where that file has been uploaded to."""
        try:
            s3.upload_fileobj(*args, ExtraArgs=ExtraArgs)
        except Exception as e:
            return str(e)
        return "{}{}".format(config('S3_LOCATION'), args[2])

    def get_matching_s3_keys(bucket, prefix='', suffix=''):
        "This will return all files that match a particular string. This is used to organize all files into a list for bulk uploading and processing"
        kwargs = {'Bucket': bucket, 'Prefix': prefix}
        while True:
            resp = s3.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
                key = obj['Key']
                if key.endswith(suffix):
                    yield key

            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    @application.route("/", methods=['GET'])
    # Minimal test route to validate app is online.
    def hello():
        return "Hello World! Welcome to Omega2020!"

    @application.route("/upload", methods=['GET'])
    # This route will load the upload page, which is a reference to validate
    # data pipelines independent of the front end being online. Handy for
    # Local Testing for the DS Team.
    def upload():
        return render_template('base.html')

    @application.route("/lines", methods=['GET'])
    # This route will load the upload page, which is a reference to validate
    # data pipelines independent of the front end being online. Handy for
    # Local Testing for the DS Team. NOTE: This template is only for testing the implementation
    # of the lines method of the Preprocess class in preprocessing.py
    def lines_test():
        return render_template('lines.html')

    @application.route("/demo_lines", methods=['GET', 'POST'])
    # This template is only for testing the implementation
    # of the lines method of the Preprocess class in preprocessing.py
    # ADD DESCRIPTIVE COMMENTS BEFORE PUSHING
    def demo_lines():
        # 
        image_file = request.files['file']
        # 
        imghash = hashlib.md5(image_file.read()).hexdigest()
        image_file.seek(0)
        # 
        imgurl = upload_file_to_s3(
            image_file,
            config('S3_BUCKET'),
            "raw_puzzles/" + imghash + '.png')

        processed, box_count, imgarray, cells = pipeline(imgurl)
        processed_image = Image.fromarray(processed)

        with BytesIO() as in_mem_file_cropped:
            processed_image.save(in_mem_file_cropped, format='PNG')
            in_mem_file_cropped.seek(0)
            processed_url = upload_file_to_s3(
                in_mem_file_cropped,
                config('S3_BUCKET'), "processed_puzzles/" +
                imghash + '_processed.png')

        return render_template('lines_results.html', imgurl=imgurl, box_count=box_count, processed_url=processed_url, cells=cells)

    @application.route("/bulk_upload", methods=['GET'])
    # This route is used for bulk upload and processing of images to bootstrap
    # our model, will take hours to run given current amount of data, but if
    # there is any alterations to the image processing pipeline, it will be
    # required to uniformly train the model on the changes.
    def bulk_upload():
        return render_template('bulk.html')

    @application.route("/demo_file", methods=['GET', 'POST'])
    # This route is the core logic of the Datascience API. Will recieve an image from a post request, and will:
    # 1. Upload Raw Image to s3.
    # 2. Run the Image Processing Pipeline, and put a copy of that processed image to S3.
    # 3. Splicing the processed image into 81 individual Sudoku cells, submitted to be scored for digit recognition, copies stored in S3.
    # 4. Takes the Numpy Array output from the image pipeline function, and loads it into a sagemaker formatted .csv file and uploads it to s3.
    # 5. Calls the Sagemaker API Endpoint referencing the S3 URL that contains the formatted CSV referenced in step 4.
    # 6. Returns the predicted digits from the Sagemaker Endpoint.
    # 7. Hands off the predicted digits from step 6 into the Solver function, and returns relevant data. (Documented in Solver.ai and ai.py)
    # 8a. For Production Use: As a JSON, returns: 1. Predicted Digits. 2. Grid Status. 3. Forecasted Difficulty of Puzzle (if solveable) 4. Solution of the puzzle (if solveable)
    # 8b. For DS Team Use: Use the commented out return argument at the end of
    # this function if you wish to use the DS page, which will display data
    # from intermediary steps of this pipeline. Very handy for DS team
    # testing, to locally validate changes.
    def demo_file():
        # Pulls the image file in the post request as a object in memory
        image_file = request.files['file']
        # Takes the hash of the image - it will be used as a unique identifer
        # across the DS API.
        imghash = hashlib.md5(image_file.read()).hexdigest()
        image_file.seek(0)
        # uploads image to raw_puzzles folder
        imgurl = upload_file_to_s3(
            image_file,
            config('S3_BUCKET'),
            "raw_puzzles/" + imghash + '.png')
        # processes the raw image, and returns the raw image to processed
        # variable and returns 81 numpy arrays (of 28x28 dimensions)
        # representing each individual sudoku cell that makes up the whole
        # puzzle
        processed, box_count, imgarray, cells = pipeline(imgurl)
        processed_image = Image.fromarray(processed)

        # loads the processed image in memory so it can be uploaded to S3 in
        # the process_puzzles folder.
        with BytesIO() as in_mem_file_cropped:
            processed_image.save(in_mem_file_cropped, format='PNG')
            in_mem_file_cropped.seek(0)
            processed_url = upload_file_to_s3(
                in_mem_file_cropped,
                config('S3_BUCKET'), "processed_puzzles/" +
                imghash + '_processed.png')

        # processes each individual suodku cell to be placed into S3.
        # This will add sevearl seconds to response time, so consider
        # commenting out when going to production once this is automated into a
        # daily batch job across newly uploaded images.
        processed_cells = []
        i = 0
        j = 0
        for array in imgarray:
            proc_img = Image.fromarray(array)
            with BytesIO() as in_mem_file:
                proc_img.convert('RGB').save(in_mem_file, format='PNG')
                in_mem_file.seek(0)
                processed_cell_url = upload_file_to_s3(
                    in_mem_file,
                    config('S3_BUCKET'),
                    "processed_cells/" +
                    imghash +
                    "_" +
                    str(i) +
                    '_cell.png')
            i = i + 1
            processed_cells.append(processed_cell_url)

        # loads all of the numpy arrays from the image processing pipeline
        allArrays = np.empty((0,))
        for array in imgarray:
            an_array = array.flatten().reshape(784,)
            allArrays = np.concatenate([allArrays, an_array])

        # reshapes the numpy array into 81 rows (one for each cell) and 784 columns (one for each value in the 784 pixels that make up a 28x28 pixel image)
        # loads it into a csv_buffer object and loaded to S3 for sagemaker
        # processing.
        if 70 < box_count < 120:
            allArrays = allArrays.reshape(81, 784)
        elif 25 < box_count < 60:
            allArrays = allArrays.reshape(36, 784)
        allArrays = np.rint(allArrays)
        csv_array = pd.DataFrame(allArrays)
        csv_buffer = StringIO()
        csv_array.to_csv(csv_buffer, header=False, index=False)

        csv_path = 'predict_payloads/' + str(imghash) + '.csv'
        csv_url = config('S3_LOCATION') + \
            str(csv_path)

        csv_buffer.seek(0)
        s3.put_object(
            Body=csv_buffer.read(),
            Bucket=config('S3_BUCKET'),
            Key=csv_path)

        # Sends an POST request to the sagemaker API URL, appending the created
        # above to the request for the sagemaker endpoint to read in. Comment the request
        # out if SageMaker is not currently running or it will produce an error.

# <<<<<<< ai-bug-fix
#         # SAGEMAKER_API_URL = config('SAGEMAKER_API_URL')
#         # data = {'data': csv_url}
#         # sagermaker_response = requests.post(SAGEMAKER_API_URL, json=data)
# =======
#         SAGEMAKER_API_URL = config('SAGEMAKER_API_URL')
#         data = {'data': csv_url}
#         #sagermaker_response = requests.post(SAGEMAKER_API_URL, json=data)
# >>>>>>> master

        # Below line is to use the AWS Sagemaker returned predictions. Comment it out, if you're testing with local models.
        #pred = sagermaker_response.content.decode('utf-8').replace("\n","").replace("0",".")

        # Below line is used for local KNN model. Comment out to use Sagemaker endpoint.
        # The web team needs to endpoint for reliability of testing, so leaving
        # it uncommented. A future release should use the sagemaker endpoint in
        # production.
        pred = predict_knn(config('MODEL_FILEPATH'), imgarray)
        # runs the predicted digits against the solver function
        # The definitions of these paramaters is documented in solver.py and
        # ai.py.

        print(f"Pred return results: {solve(str(pred))}")
        grid_status = solve(str(pred))[0]
        solution = solve(str(pred))[1]
        difficulty = solve(str(pred))[3]

        # In the event a puzzle has invalid values, remapping from backend to
        # frontend is required for the front end to highlight invalid cells
        # (web team did not get this functionality in final launch, but leaving
        # it in for a future release as DS team functionality is ready)
        if len(list(solve(str(pred))[1])) != 81 and grid_status == 2:
            errors = list(solve(str(pred))[1])
            for e in errors:
                error_pairs = []
                if e == '':
                    pass
                else:
                    guess_pair = []
                    guess = e[0]
                    cell = find_replace_multi(e[1], translation_dictionary)
                    guess_pair.append(guess)
                    guess_pair.append(cell)
                    error_pairs.append(guess_pair)
                solution = error_pairs
        else:
            pass

        # db_csv = pd.DataFrame()
        # for i in range(len(pred)):
        #     db_csv['pred'][i] = pred[i]
        # for i in range(len(processed_cell_url)):
        #     db_csv['cell_url'][i] =  processed_cell_url[i]

        # If the puzzle is solveable, adding the numpy arrays for the sudoku
        # cells into the ModelTrainer Database for future image training.
        if grid_status == 1:
            for i in range(len(imgarray)):
                #outfile = TemporaryFile()
                #np.save(outfile, imgarray[i])
                #import pdb; pdb.set_trace()
                # stitch predicted class with S3 URL and Numpy Array

                entry = ModelTrainer(
                    sudoku_hash=imghash,
                    procesed_puzzle_url=processed_url,
                    cell_url=processed_cells[i],
                    numpy_array=imgarray[i].flatten().tolist(),
                    predicted_value=pred[i])
                DB.session.add(entry)
                DB.session.commit()

        # This template is used if you want to use the DS view (referenced in step 8b)
        # return render_template(
        #     'results.html',
        #     imghash=imghash,
        #     imgurl=imgurl,
        #     pred=pred,
        #     processed_url=processed_url,
        #     processed_cells=processed_cells,
        #     original_grid=original_grid,
        #     solved=solution,
        #     grid_status=grid_status)

        # This is the production API response to use for web team
        # functionality.
        return jsonify(values=pred, puzzle_status=grid_status,
                       solution=solution, difficulty=difficulty)

    @application.route("/bulk_processing", methods=['GET'])
    # This route is to be used to batch rerun image procesisng pipelines across all raw images in the raw_images folder.
    # THIS ROUTE IS NOT USED IN PRODUCTION, but it will allow automated re-processing of images to streamline future optimizations.
    # This route was handy when the team took 500+ pictures of sudoku puzzles
    # to help bootstrap training our own model.
    def bulk_processing():

        start_url = config('S3_LOCATION')
        # creates a list of all S3 URLs of raw images in the S3 bucket.
        all_files = get_matching_s3_keys(S3_BUCKET, 'raw_images/', '.png')

        clean_urls = []
        urls = list(all_files)
        for a_url in urls:
            a_url = str(a_url)
            new_url = a_url.replace(" ", "+")
            new_url = start_url + new_url
            clean_urls.append(new_url)
        x = 0

        # loops through each image organized above and processed using the
        # pipeline function, then subdividies it into 81 sudoku cells and
        # uploads each cell.
        for url in clean_urls:
            img_url = url
            request = urllib.request.Request(img_url)
            img = urllib.request.urlopen(request)

            imghash = hashlib.md5(img.read()).hexdigest()
            processed, imgarray = pipeline(img_url)
            processed_image = Image.fromarray(processed)
            with BytesIO() as in_mem_file_cropped:
                processed_image.save(in_mem_file_cropped, format='PNG')
                in_mem_file_cropped.seek(0)
                upload_file_to_s3(
                    in_mem_file_cropped,
                    config('S3_BUCKET'),
                    "processed_puzzles/" + imghash + '_bulk_processed.png')

            processed_cells = []
            i = 0
            for array in imgarray:
                proc_img = Image.fromarray(array)
                with BytesIO() as in_mem_file:
                    proc_img.convert('RGB').save(in_mem_file, format='PNG')
                    in_mem_file.seek(0)
                    upload_file_to_s3(
                        in_mem_file,
                        config('S3_BUCKET'),
                        "processed_cells/" + imghash +
                        "_" +
                        str(i) +
                        '_bulk_cell.png')
                i = i + 1

            print("This is file " + str(x) + " out of " + str(len(clean_urls)))
            x = x + 1
            print(str(img_url) + " has been uploaded!")

        return render_template('bulk_results.html', uploaded_files=clean_urls)

    # Route that will reset and initialize the databases.
    @application.route("/reset", methods=['GET'])
    def reset():
        # sets the .csv of reference sudoku puzzles and populates it into a
        # Postgres database called PuzzleTable.
        path = 'data/dataset.csv'
        df = pd.read_csv(path)

        DB.drop_all()
        DB.create_all()

        #Applies full dataframe to database
        for i in range(len(df)):
        # uncomment if you are testing rewriting tables, and don't want to wait for the entire reference table to be loaded (takes ~5 minutes)
        #for i in range(100):
            aid = df['Id'][i]
            aid = int(aid)
            asudoku = df['Sudoku'][i]
            asolution = df['Solution'][i]
            alevel = df['Level'][i]
            apeople = df['People'][i]
            aavg_time = df['Average-Time'][i]
            apeople = int(apeople)
            aavg_time = int(aavg_time)
            asudoku_hash = hashlib.md5(asudoku.encode('utf-8')).hexdigest()
            entry = PuzzleTable(
                id=aid,
                sudoku=asudoku,
                solution=asolution,
                level=alevel,
                people=apeople,
                avg_time=aavg_time,
                sudoku_hash=asudoku_hash)
            DB.session.add(entry)
            DB.session.commit()
            print("Row " + str(i) + " out of: " + str(len(df)) + " completed.")
        return "Database Reset!"

    @application.route("/solve", methods=['GET', 'POST'])
    # Will take inbound sudoku puzzle strings from the front end, and will run it against the solver code.
    # Detail of code documented above in demo_file route.
    def solve_sudoku():
        pred = request.args.get("puzzle")
        solved = solve(str(pred))
        grid_status = solved[0]
        #print(grid_status)
        solution = solved[1]
        #print(solution)
        difficulty = solved[3]
        print(len(list(solution)))
        if len(list(solution)) in [16, 36, 81, 144, 256]:
            pass
        else:# len(list(solution)) != 81 or len(list(solution)) != 16 or len(list(solution)) != 36 or len(list(solution)) != 144 or len(list(solution)) != 256:
            errors = list(solution)
            print(f'Here are the errors: {errors}')
            for e in errors:
                error_pairs = []
                if e == '':
                    pass
                else:
                    print(f'This is e: {e}')
                    guess_pair = []
                    guess = e[0]
                    if len(pred) == 14:
                        translation = translation_dictionary4
                    elif len(pred) == 36:
                        translation = translation_dictionary6
                    elif len(pred) == 81:
                        translation = translation_dictionary
                    elif len(pred) == 144:
                        translation = translation_dictionary12
                    elif len(pred) == 256:
                        translation = translation_dictionary16
                    cell = find_replace_multi(e[1], translation)
                    guess_pair.append(guess)
                    guess_pair.append(cell)
                    error_pairs.append(guess_pair)
                solution = error_pairs
        # else:
        #     pass
        return jsonify(
            values=pred,
            puzzle_status=grid_status,
            solution=solution,
            difficulty=difficulty)

    @application.route("/train", methods=['GET', 'POST'])
    def train_model():
        # Function to pull all valid uploaded Sudoku puzzles, removes duplicate values, and parses into a Sagemaker valid format.
        # First column is predicted outcome, then 784 columns for each value in
        # the 28x28 Numpy Array representing each Sudoku cell image.

        # Configures the DB connection to the ModelTrainer table.
        t_host = config('TRAIN_DATABASE_HOST')
        t_port = "5432"
        t_dbname = config('TRAIN_DATABASE_TABLE')
        t_user = config('TRAIN_DATABASE_USER')
        t_pw = config('TRAIN_DATABASE_PW')
        db_conn = psycopg2.connect(
            host=t_host,
            port=t_port,
            dbname=t_dbname,
            user=t_user,
            password=t_pw)
        db_cursor = db_conn.cursor()

        new_data = pd.DataFrame(columns=range(785))
        model_train_query = '''SELECT predicted_value, numpy_array FROM "model_trainer";'''

        # Queries the ModelTrainer table
        values = ModelTrainer.query.all()
        df = pd.read_sql_query(model_train_query, con=db_conn)

        # removing wrapper brackets, and reverses the . character to 0 for
        # model training
        df['numpy_array'] = df['numpy_array'].str.strip("}")
        df['numpy_array'] = df['numpy_array'].str.strip("{")
        df['predicted_value'] = df['predicted_value'].replace(".", "0")

        # for each row in the dataframe, expands out the Numpy Array to the
        # same format as the Sagemaker endpoint.
        pixel_values = []
        for i in range(len(df['numpy_array'])):
            pixels = df['numpy_array'][i].split(",")
            pixel_values.append(pixels)
        pixels_df = pd.DataFrame(pixel_values)

        # maps the pixel dataframe to the final dataframe values
        # i+1 is used because the first column is for the predicted digit.
        final_df = pd.DataFrame(columns=range(785))
        for i in range(784):
            final_df[(i + 1)] = pixels_df[i]

        # assigning the predicted digit to the first column of the final
        # dataframe
        final_df[0] = df['predicted_value']

        # writes the final_df CSV to a validator folder in s3.
        # not written directly to the train folder, as it has not been validated that each uploaded predicted cell was accurate
        # to be included in a future release.
        train_csv_path = "pre_validated_data/new_data.csv"
        csv_buffer_train = StringIO()
        final_df = final_df.drop_duplicates()
        final_df.to_csv(csv_buffer_train, header=False, index=False)
        csv_buffer_train.seek(0)
        s3.put_object(
            Body=csv_buffer_train.read(),
            Bucket=config('S3_BUCKET'),
            Key=train_csv_path)
        return "Done! Scored images uploaded to s3 to sagemaker pipeline!"

    return application

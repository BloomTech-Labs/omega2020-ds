from flask import Flask, redirect, flash, request, render_template, jsonify
from schema import DB, PuzzleTable, ModelTrainer
from decouple import config
from pipeline import *
import boto3
import requests
import hashlib
import pandas as pd
import cv2
import json
import hashlib
import scipy.misc
from PIL import Image
from io import BytesIO, StringIO
from werkzeug.utils import secure_filename
import urllib.request
import sys
import logging
import re
from flask_cors import CORS
from urllib.request import urlopen
import json
from tempfile import TemporaryFile
import psycopg2

from ai import *
from solver import *
from dictionary import translation_dictionary


def init_db():
    path = 'data/dataset.csv'
    df = pd.read_csv(path)


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def create_app():
    # global variables within the flask app including the app name, and the DB Configuration path
    # .env file will specify production vs. development enviornment.
    application = Flask(__name__)
    CORS(application)
    application.debug = True
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)
    application.logger.addHandler(stream_handler)
    application.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    application.config['ENV'] = config('FLASK_ENV')
    application.config['DEBUG'] = config('FLASK_DEBUG')
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    DB.init_app(application)
    model_path = config('MODEL_FILEPATH')

    AWS = {
        'aws_access_key_id': config('S3_KEY'),
        'aws_secret_access_key': config('S3_SECRET')
    }
    ExtraArgs = json.loads(config('ExtraArgs'))
    s3 = boto3.client("s3", **AWS)

    S3_BUCKET = config('S3_BUCKET')
    S3_LOCATION = config('S3_LOCATION')

    def find_replace_multi(string, dictionary):
        for item in dictionary.keys():
            # sub item for item's paired value in string
            string = re.sub(item, dictionary[item], string)
        return string

    def upload_file_to_s3(*args):
        try:
            s3.upload_fileobj(*args, ExtraArgs=ExtraArgs)
        except Exception as e:
            return str(e)
        return "{}{}".format(config('S3_LOCATION'), args[2])

    def get_matching_s3_keys(bucket, prefix='', suffix=''):
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
    def hello():
        return "Hello World!"

    @application.route("/upload", methods=['GET'])
    def upload():
        return render_template('base.html')

    @application.route("/bulk_upload", methods=['GET'])
    def bulk_upload():
        return render_template('bulk.html')

    @application.route("/demo_file", methods=['GET', 'POST'])
    def demo_file():
        image_file = request.files['file']
        imghash = hashlib.md5(image_file.read()).hexdigest()
        image_file.seek(0)
        imgurl = upload_file_to_s3(
            image_file,
            config('S3_BUCKET'),
            "raw_images/"+imghash + '.png')
        processed, imgarray = pipeline(imgurl)
        processed_image = Image.fromarray(processed)
        with BytesIO() as in_mem_file_cropped:
            processed_image.save(in_mem_file_cropped, format='PNG')
            in_mem_file_cropped.seek(0)
            processed_url = upload_file_to_s3(
                in_mem_file_cropped,
                config('S3_BUCKET'), "processed_puzzles/" +
                imghash + '_processed.png')

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

        allArrays = np.empty((0,))
        for array in imgarray:
            an_array = array.flatten().reshape(784,)
            allArrays = np.concatenate([allArrays, an_array])

        allArrays = allArrays.reshape(81, 784)
        allArrays = np.rint(allArrays)
        csv_array = pd.DataFrame(allArrays)
        csv_buffer = StringIO()
        csv_array.to_csv(csv_buffer, header=False, index=False)

        csv_path = 'predict_payloads/' + str(imghash) + '.csv'
        csv_url = "https://omega2020-sagemaker.s3.amazonaws.com/" + \
            str(csv_path)

        upload_file_to_s3(image_file, config('S3_BUCKET'), imghash + '.png')

        csv_buffer.seek(0)
        s3.put_object(
            Body=csv_buffer.read(),
            Bucket='omega2020-sagemaker',
            Key=csv_path)

        SAGEMAKER_API_URL = 'https://9g1ep6et2m.execute-api.us-east-1.amazonaws.com/test/omega-predict-digits/'
        data = {'data': csv_url}
        sagermaker_response = requests.post(SAGEMAKER_API_URL, json=data)

        #pred = sagermaker_response.content.decode('utf-8').replace("\n","").replace("0",".")
        #import pdb; pdb.set_trace()

        # KNN predictions ran locally, not needed with sagemaker online.
        pred = predict_knn(config('MODEL_FILEPATH'), imgarray)

        original_grid = "test_value"

        grid_status = solve(str(pred))[0]
        solution = solve(str(pred))[1]
        difficulty = solve(str(pred))[3]

        if len(list(solve(str(pred))[1])) != 81 & grid_status == 2:

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
        return jsonify(values=pred, puzzle_status=grid_status,
                       solution=solution, difficulty=difficulty)

    @application.route("/bulk_processing", methods=['GET'])
    def bulk_processing():
        start_url = 'https://omega2020.s3.amazonaws.com/'

        all_files = get_matching_s3_keys(S3_BUCKET, 'raw_puzzles', '.png')

        clean_urls = []
        urls = list(all_files)
        for a_url in urls:
            a_url = str(a_url)
            new_url = a_url.replace(" ", "+")
            new_url = start_url + new_url
            clean_urls.append(new_url)
        x = 0

        for url in clean_urls:

            img_url = url
            request = urllib.request.Request(img_url)
            img = urllib.request.urlopen(request)

            imghash = hashlib.md5(img.read()).hexdigest()
            # img.seek(0)
            #imgurl = upload_file_to_s3(img, config('S3_BUCKET'), imghash+'_bulk_raw.png')
            processed, imgarray = pipeline(img_url)
            processed_image = Image.fromarray(processed)
            with BytesIO() as in_mem_file_cropped:
                processed_image.save(in_mem_file_cropped, format='PNG')
                in_mem_file_cropped.seek(0)
                upload_file_to_s3(
                    in_mem_file_cropped,
                    config('S3_BUCKET'),
                    imghash + '_bulk_processed.png')

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
                        imghash +
                        "_" +
                        str(i) +
                        '_bulk_cell.png')
                i = i + 1

            print("This is file " + str(x) + " out of " + str(len(clean_urls)))
            x = x + 1
            print(str(img_url) + " has been uploaded!")

        return render_template('bulk_results.html', uploaded_files=clean_urls)

    # route that will reset the database.
    @application.route("/reset", methods=['GET'])
    def reset():
        path = 'data/dataset.csv'
        df = pd.read_csv(path)

        DB.drop_all()
        DB.create_all()

        # for i in range(len(df)):
        for i in range(100):
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
    def solve_sudoku():
        pred = request.args.get("puzzle")
        grid_status = solve(str(pred))[0]
        solution = solve(str(pred))[1]
        difficulty = solve(str(pred))[3]
        if len(list(solve(str(pred))[1])) != 81:

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
        return jsonify(
            values=pred,
            puzzle_status=grid_status,
            solution=solution,
            difficulty=difficulty)

    @application.route("/train", methods=['GET', 'POST'])
    def train_model():
        # Function to pull in Values from Database matching train_data format
        # remove duplicate values
        # pass array and predicted class into .csv format
        # first column is predicted outcome, then 784 columns for each value in
        # the array.

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
        values = ModelTrainer.query.all()
        df = pd.read_sql_query(model_train_query, con=db_conn)

        df['numpy_array'] = df['numpy_array'].str.strip("}")
        df['numpy_array'] = df['numpy_array'].str.strip("{")
        df['predicted_value'] = df['predicted_value'].replace(".", "0")
        pixel_values = []
        for i in range(len(df['numpy_array'])):
            pixels = df['numpy_array'][i].split(",")
            pixel_values.append(pixels)

        pixels_df = pd.DataFrame(pixel_values)

        final_df = pd.DataFrame(columns=range(785))
        for i in range(784):
            final_df[(i + 1)] = pixels_df[i]

        final_df[0] = df['predicted_value']

        train_csv_path = "pre_validated_data/new_data.csv"
        csv_buffer_train = StringIO()
        final_df.to_csv(csv_buffer_train, header=False, index=False)
        csv_buffer_train.seek(0)
        s3.put_object(
            Body=csv_buffer_train.read(),
            Bucket='omega2020-sagemaker',
            Key=train_csv_path)
        return "Done! Scored images uploaded to s3 to sagemaker pipeline!"

    return application

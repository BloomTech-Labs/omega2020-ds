from flask import Flask, redirect, url_for, flash, request, render_template, copy_current_request_context, jsonify
from schema import DB, PuzzleTable
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


from ai import * 
from solver import *

def init_db():
    path = 'data/dataset.csv'
    df = pd.read_csv(path)

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


def create_app():
    #global variables within the flask app including the app name, and the DB Configuration path
    #.env file will specify production vs. development enviornment.
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

    S3_BUCKET =  config('S3_BUCKET')
    S3_LOCATION = config('S3_LOCATION')


    def find_replace_multi(string, dictionary):
        for item in dictionary.keys():
            # sub item for item's paired value in string
            string = re.sub(item, dictionary[item], string)
        return string

    def upload_file_to_s3(*args):
        try: s3.upload_fileobj(*args, ExtraArgs=ExtraArgs)
        except Exception as e: return str(e)
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
        imgurl = upload_file_to_s3(image_file, config('S3_BUCKET'), imghash+'.png')
        processed, imgarray = pipeline(imgurl)
        processed_image = Image.fromarray(processed)
        with BytesIO() as in_mem_file_cropped:
            processed_image.save(in_mem_file_cropped, format='PNG')
            in_mem_file_cropped.seek(0)
            processed_url = upload_file_to_s3(in_mem_file_cropped, config('S3_BUCKET'), imghash+'_processed.png')

        processed_cells = []
        i = 0
        j = 0
        for array in imgarray:
            proc_img = Image.fromarray(array)
            with BytesIO() as in_mem_file:
                proc_img.convert('RGB').save(in_mem_file, format='PNG')
                in_mem_file.seek(0)
                processed_cell_url = upload_file_to_s3(in_mem_file, config('S3_BUCKET'), imghash+"_"+str(i)+'_cell.png')
            i = i+1
            processed_cells.append(processed_cell_url)
        
        #CNN Model Here:
        #pred = predict(imgarray)
        #KNN Prediction Here:
        pred = predict_knn(config('MODEL_FILEPATH'),imgarray)
        
        original_grid = "test_value"
        #import pdb; pdb.set_trace()
        grid_status = solve(str(pred))[0]
        solution = solve(str(pred))[1]

        translation_dictionary = {
            "A1": "00",
            "A2": "01",
            "A3": "02",
            "A4": "03",
            "A5": "04",
            "A6": "05",
            "A7": "06",
            "A8": "07",
            "A9": "08",
            "B1": "10",
            "B2": "11",
            "B3": "13",
            "B4": "14",
            "B5": "15",
            "B6": "15",
            "B7": "16",
            "B8": "17",
            "B9": "18",
            "C1": "20",
            "C2": "21",
            "C3": "23",
            "C4": "23",
            "C5": "24",
            "C6": "25",
            "C7": "26",
            "C8": "27",
            "C9": "28",
            "D1": "30",
            "D2": "31",
            "D3": "32",
            "D4": "33",
            "D5": "34",
            "D6": "35",
            "D7": "36",
            "D8": "37",
            "D9": "38",
            "E1": "40",
            "E2": "41",
            "E3": "42",
            "E4": "43",
            "E5": "44",
            "E6": "45",
            "E7": "46",
            "E8": "47",
            "E9": "48",
            "F1": "50",
            "F2": "51",
            "F3": "52",
            "F4": "53",
            "F5": "54",
            "F6": "55",
            "F7": "56",
            "F8": "57",
            "F9": "58",
            "G1": "60",
            "G2": "61",
            "G3": "62",
            "G4": "63",
            "G5": "64",
            "G6": "65",
            "G7": "66",
            "G8": "67",
            "G9": "68",
            "H1": "70",
            "H2": "71",
            "H3": "72",
            "H4": "73",
            "H5": "74",
            "H6": "75",
            "H7": "76",
            "H8": "77",
            "H9": "78",
            "I1": "80",
            "I2": "81",
            "I3": "82",
            "I4": "83",
            "I5": "84",
            "I6": "85",
            "I7": "86",
            "I8": "87",
            "I9": "88",
        }
        if len(list(solve(str(pred))[1])) != 81:

            errors = list(solve(str(pred))[1])
            for e in errors:
                error_pairs = []
                if e =='':
                    pass
                else:
                    guess_pair = []
                    guess = e[0]
                    cell = find_replace_multi(e[1],translation_dictionary)
                    guess_pair.append(guess)
                    guess_pair.append(cell)
                    error_pairs.append(guess_pair)
                solution = error_pairs
        else:
            pass
        
        #return render_template('results.html', imghash = imghash, imgurl = imgurl, pred=pred, processed_url=processed_url, processed_cells=processed_cells,original_grid=original_grid,solved=solved)
        return jsonify(values = pred, puzzle_status=grid_status, solution=solution)



    
    @application.route("/bulk_processing", methods=['GET'])
    def bulk_processing():
        start_url = 'https://omega2020.s3.amazonaws.com/'

        all_files = get_matching_s3_keys(S3_BUCKET, 'raw_puzzles', '.png')

        clean_urls = []
        urls = list(all_files)
        for a_url in urls:
            a_url = str(a_url)
            new_url = a_url.replace(" ","+")
            new_url = start_url + new_url
            clean_urls.append(new_url)
        x = 0

        for url in clean_urls:

            img_url = url
            request = urllib.request.Request(img_url)
            img = urllib.request.urlopen(request)

            imghash = hashlib.md5(img.read()).hexdigest()
            #img.seek(0)
            #imgurl = upload_file_to_s3(img, config('S3_BUCKET'), imghash+'_bulk_raw.png')
            processed, imgarray = pipeline(img_url)
            processed_image = Image.fromarray(processed)
            with BytesIO() as in_mem_file_cropped:
                processed_image.save(in_mem_file_cropped, format='PNG')
                in_mem_file_cropped.seek(0)
                upload_file_to_s3(in_mem_file_cropped, config('S3_BUCKET'), imghash+'_bulk_processed.png')

            processed_cells = []
            i = 0
            for array in imgarray:
                proc_img = Image.fromarray(array)
                with BytesIO() as in_mem_file:
                    proc_img.convert('RGB').save(in_mem_file, format='PNG')
                    in_mem_file.seek(0)
                    upload_file_to_s3(in_mem_file, config('S3_BUCKET'), imghash+"_"+str(i)+'_bulk_cell.png')
                i = i+1
                
            print("This is file "+ str(x)+" out of "+str(len(clean_urls)))
            x = x+1
            print(str(img_url)+" has been uploaded!")
            

        return render_template('bulk_results.html', uploaded_files=clean_urls)


    

    #route that will reset the database.
    @application.route("/reset", methods=['GET'])
    def reset():
        path = 'data/dataset.csv'
        df = pd.read_csv(path)

        DB.drop_all()
        DB.create_all()

        for i in range(len(df)):
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
            entry = PuzzleTable(id= aid,sudoku= asudoku,solution=asolution,level=alevel,people=apeople,avg_time=aavg_time,sudoku_hash=asudoku_hash)
            DB.session.add(entry)
            DB.session.commit()
            print("Row "+str(i)+" out of: "+str(len(df))+" completed.")
        return "Database Reset!"
    return application
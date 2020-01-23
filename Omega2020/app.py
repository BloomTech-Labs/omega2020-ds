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
    application.debug = True
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)
    application.logger.addHandler(stream_handler)
    logging.basicConfig(filename='/opt/python/log/my.log',level=logging.INFO)
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

        processed_cells = chunks(processed_cells,9)

        
        #CNN Model Here:
        #pred = predict(imgarray)
        #KNN Prediction Here:
        pred = predict_knn(config('MODEL_FILEPATH'),imgarray)
        
        original_grid = "."
        #import pdb; pdb.set_trace()
        grid_status = solve(pred)[0]
        if grid_status == 'Ivalid Sudoku, check these values:':
            solved_grid = "Invalid Puzzle"
            solved = "Invalid Puzzle"
        else:
            solved_grid = solve(pred)[2]
            #import pdb; pdb.set_trace()
            solved = display(solved_grid)


        
        #return render_template('results.html', imghash = imghash, imgurl = imgurl, pred=pred, processed_url=processed_url, processed_cells=processed_cells,original_grid=original_grid,solved=solved)
        return jsonify(values = pred, puzzle_status=grid_status, solution=solve(pred)[1])



    
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
        path = 'Omega2020/data/dataset.csv'
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
        return "Database Reset!"
    return application
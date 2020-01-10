from flask import Flask, redirect, url_for, flash, request, render_template
from .schema import DB, PuzzleTable
from decouple import config
from .pipeline import *
import boto3
import requests
import hashlib
import pandas as pd
import cv2
import json
import hashlib
import scipy.misc
from PIL import Image
from io import BytesIO

def init_db():
    path = 'data/dataset.csv'
    df = pd.read_csv(path)



def create_app():
    #global variables within the flask app including the app name, and the DB Configuration path
    #.env file will specify production vs. development enviornment.
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('FLASK_ENV')
    app.config['DEBUG'] = config('FLASK_DEBUG')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    DB.init_app(app)
    model_path = config('MODEL_FILEPATH')

    AWS = {
    'aws_access_key_id': config('S3_KEY'),
    'aws_secret_access_key': config('S3_SECRET')
    }
    ExtraArgs = json.loads(config('ExtraArgs'))
    s3 = boto3.client("s3", **AWS)
    def upload_file_to_s3(*args):
        try: s3.upload_fileobj(*args, ExtraArgs=ExtraArgs)
        except Exception as e: return str(e)
        return "{}{}".format(config('S3_LOCATION'), args[2])

    S3_BUCKET =  config('S3_BUCKET')
    S3_LOCATION = config('S3_LOCATION')






    @app.route("/")
    def hello():
        return "Hello World!"

    @app.route("/upload")
    def upload():
        return render_template('base.html')

    @app.route("/demo_file", methods=['GET', 'POST'])
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
        for array in imgarray:
            proc_img = Image.fromarray(array)
            with BytesIO() as in_mem_file:
                proc_img.save(in_mem_file, format='PNG')
                in_mem_file.seek(0)
                processed_cell_url = upload_file_to_s3(in_mem_file, config('S3_BUCKET'), imghash+"_"+str(i)+'_cell.png')
            i = i+1
            processed_cells.append(processed_cell_url)
        pred = predict(imgarray)
        return render_template('results.html', imghash = imghash, imgurl = imgurl, pred=pred, processed_url=processed_url, processed_cells=processed_cells)

    #route that will reset the database.
    @app.route("/reset")
    def reset():
        path = model_path
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
    return app

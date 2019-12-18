from flask import Flask, redirect, url_for, flash, request, render_template
from Omega2020.schema import DB, PuzzleTable
from decouple import config


import hashlib
import pandas as pd

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


    @app.route("/")
    def hello():
        return "Hello World!"


    #route that will reset the database.    
    @app.route("/reset")
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
    return app
from flask import Flask, redirect, url_for, flash, request, render_template
from Omega2020.schema import DB
from decouple import config

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('FLASK_ENV')
    app.config['DEBUG'] = config('FLASK_DEBUG')
    DB.init_app(app)


    @app.route("/")
    def hello():
        return "Hello World!"


    #route that will reset the database.    
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return "Database Reset!"
    return app
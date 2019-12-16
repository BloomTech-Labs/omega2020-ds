from flask import Flask, redirect, url_for, flash, request, render_template

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def hello():
        return "Hello World!"
    return app
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

#A minimal Database with two values: ID for a Puzzle and the values that puzzle holds.
class Puzzle(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    values = DB.Column(DB.String(200), nullable=False)
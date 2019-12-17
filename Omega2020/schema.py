from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

#A minimal Database with two values: ID for a Puzzle and the values that puzzle holds.
class PuzzleTable(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    sudoku = DB.Column(DB.String(200), nullable=False)
    solution = DB.Column(DB.String(200), nullable=False)
    level = DB.Column(DB.String(200), nullable=False)
    people = DB.Column(DB.Integer, nullable=False)
    avg_time = DB.Column(DB.String(500), nullable=False)
    sudoku_hash = DB.Column(DB.String(100), nullable=False)


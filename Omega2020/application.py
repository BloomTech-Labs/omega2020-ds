from app import create_app
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

application = create_app()

if __name__ == '__main__':
    application.debug = True
    application.run()
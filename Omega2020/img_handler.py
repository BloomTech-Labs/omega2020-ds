import io
import os
import hashlib
import requests
import json
from decouple import config
from werkzeug.utils import secure_filename
import boto3, botocore

from PIL import Image

# constants
IMGDIR_PATH = 'PicMetric/assets/temp'
UPLOAD_FOLDER = 'PicMetric/assets/temp/'
ExtraArgs = json.loads(config('ExtraArgs'))

# instantiate S3
AWS = {
    'aws_access_key_id': config('S3_KEY'),
    'aws_secret_access_key': config('S3_SECRET')
}
s3 = boto3.client("s3", **AWS)


def upload_file_to_s3(*args):
    try: s3.upload_fileobj(*args, ExtraArgs=ExtraArgs)
    except Exception as e: return str(e)
    return "{}{}".format(config('S3_LOCATION'), args[2])
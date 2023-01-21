from App import app
from flask import render_template, url_for, redirect, flash, request, session, jsonify
from werkzeug.utils import secure_filename
import uuid, os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from threading import Thread
from time import sleep
import cv2

from matplotlib import pyplot as plt

import sys
sys.path.insert(1, '/home/michal/repo/road-sign-checker/ai/sign-classificators/img_scripts')
from img_scripts import crop_image as ci


limiter = Limiter(get_remote_address,app=app,storage_uri="memory://")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def pipeline(uid):
    filepath_img = "/".join([app.config['UPLOAD_FOLDER'], uid + '.jpg'])
    filepath_mask = "/".join([app.config['UPLOAD_FOLDER'], uid + '_mask.jpg'])
    mask = ci.getFinalMaskFromImage(filepath_img)
    cv2.imwrite(filepath_mask, mask)
    #TODO

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
@limiter.limit("10/minute")
@limiter.limit("1/second")
def upload():
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    
    print(request.files)
    if '' not in request.files:
        return jsonify({"info":"File key not found"})
    
    uid = str(uuid.uuid4())
        
    file = request.files['']
    filename = secure_filename(uid+'.jpg')
    destination="/".join([app.config['UPLOAD_FOLDER'], filename])
    file.save(destination)
    
    thread = Thread(target=pipeline, kwargs={"uid":uid})
    thread.start()
    
    return jsonify({"info":"File successfully saved","uid":uid})
    

        
@app.route('/info', methods=['POST'])
@limiter.limit("1/second")
def info():
    
    if not os.path.isdir(app.config['DOWNLOAD_FOLDER']):
        os.mkdir(app.config['DOWNLOAD_FOLDER'])
    
    uid = str(request.get_json()['uid'])
    filepath = "/".join([app.config['DOWNLOAD_FOLDER'], uid + '.txt'])
    if not os.path.isfile(filepath):
        return jsonify({"info":"Info about uid='" + uid + "' not found"})
    
    #TODO

    return jsonify({"uid":uid})




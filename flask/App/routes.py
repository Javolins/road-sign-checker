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
from img_scripts import image_analisys_functions as iaf
from img_scripts import classifier_color as cc
import numpy

limiter = Limiter(get_remote_address,app=app,storage_uri="memory://")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def pipeline(uid):
    filepath_img = "/".join([app.config['UPLOAD_FOLDER'], uid + '.jpg'])
    filepath_mask = "/".join([app.config['UPLOAD_FOLDER'], uid + '_mask.jpg'])
    mask = ci.getFinalMaskFromImage(filepath_img)
    cv2.imwrite(filepath_mask, mask)
    print(iaf.getShape(mask))
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
    if 'userImg' not in request.files:
        return jsonify({"info":"File key not found"})
    
    uid = str(uuid.uuid4())
        
    file = request.files['userImg']
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


def uposledzony_pipeline():
    filepath_img = '/home/michal/repo/road-sign-checker/flask/App/static/photos/6db324da-a096-4872-ba58-b1231f4badc1.jpg'
    filepath_mask = '/home/michal/repo/road-sign-checker/flask/App/static/photos/6db324da-a096-4872-ba58-b1231f4badc1_mask.jpg'
    mask = ci.getFinalMaskFromImage(filepath_img)
    cv2.imwrite(filepath_mask, mask)
    # print(numpy.ndarray(mask))
    # print(iaf.getShape(cv2.cvtColor(cv2.cvtColor(mask, cv2.COLOR_HSV2RGB), cv2.COLOR_RGBA2GRAY)))
    dictionary = {}
    dictionary['finalColorClasifaier'] = cc.finalColorClasifaier(ci.readImageAsRGB(filepath_img), mask)
    #TODO

@app.route('/kurwamac', methods=['GET'])
@limiter.limit("1/second")
def kurwamac():
    thread = Thread(target=uposledzony_pipeline)
    thread.start()
    
    return jsonify({"info":"XDD","uid":0})
from App import app
from flask import render_template, url_for, redirect, flash, request, session, jsonify
from werkzeug.utils import secure_filename
import uuid, os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from threading import Thread
from time import sleep
import cv2
import json
import pathlib
import numpy

from matplotlib import pyplot as plt

import sys
sys.path.insert(1, '/home/michal/repo/road-sign-checker/ai/sign-classificators/img_scripts')
from img_scripts import crop_image as ci
from img_scripts import image_analisys_functions as iaf
from img_scripts import classifier_color as cc
from img_scripts import sign_classifier as sc
from img_scripts import nnpaths as nn

limiter = Limiter(get_remote_address,app=app,storage_uri="memory://")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def pipeline(uid, deletePhotos):
    filepath_img = "/".join([app.config['UPLOAD_FOLDER'], uid + '.jpg'])
    filepath_mask = "/".join([app.config['UPLOAD_FOLDER'], uid + '_mask.jpg'])
    filepath_json = "/".join([app.config['DOWNLOAD_FOLDER'], uid + '.json'])
    
    mask = ci.getFinalMaskFromImage(filepath_img)
    cv2.imwrite(filepath_mask, mask)
    
    info = {}
    info['maskShape'] = str(iaf.getMaskShape(mask))
    if info['maskShape'] == 'ZnakShape.OCTAGON' or info['maskShape'] == 'ZnakShape.UNKNOWN':
        with open(filepath_json, "w") as outfile:
            json.dump(info, outfile)
        return
    info['finalColorClasifaier'] = cc.finalColorClasifaier(ci.readImageAsRGB(filepath_img), mask)
    
    max_value = max(info['finalColorClasifaier'])
    max_index = info['finalColorClasifaier'].index(max_value)
    sign_type = 0

    if max_index == 0:
        sign_type = nn.SignType.WARNING.value
    if max_index == 1:
        sign_type = nn.SignType.PROHIBITION.value
    if max_index == 2:
        sign_type = nn.SignType.WARRANT_INFORMATIONAL.value
        
    path_builder = nn.SignsNeuralNetworkPathBuilers('/home/michal/repo/road-sign-checker/ai/sign-classificators')
    model_path = path_builder.getModelPath(sign_type)
    # print(type(model_path))
    # print(model_path)
    # print(type(os.path.abspath(model_path)))
    classifier = sc.SignClassifier(pathlib.Path(model_path).as_posix())
    result = classifier.preprocessAndClassify(cv2.imread(filepath_img),mask)
    
    info['classifiedType'] = result.getClassifiedType()
    
    with open(filepath_json, "w") as outfile:
        json.dump(info, outfile)
    
    print(info)
    if deletePhotos:
        os.remove(filepath_img)
        os.remove(filepath_mask)
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
    
    if 'userImg' not in request.files:
        return jsonify({"info":"File key not found"})
    
    uid = str(uuid.uuid4())
        
    file = request.files['userImg']
    filename = secure_filename(uid+'.jpg')
    destination="/".join([app.config['UPLOAD_FOLDER'], filename])
    file.save(destination)
    
    image_size = numpy.shape(ci.readImageAsRGB(destination))
    if image_size[0] != image_size[1]:
        os.remove(destination)
        return jsonify({"info":"Image is not a square!"})
        
    thread = Thread(target=pipeline, kwargs={"uid":uid,"deletePhotos":True})
    thread.start()
    
    return jsonify({"info":"File successfully saved","uid":uid})
    

        
@app.route('/info', methods=['POST'])
@limiter.limit("1/second")
def info():
    
    if not os.path.isdir(app.config['DOWNLOAD_FOLDER']):
        os.mkdir(app.config['DOWNLOAD_FOLDER'])
    
    uid = str(request.get_json()['uid'])
    filepath = "/".join([app.config['DOWNLOAD_FOLDER'], uid + '.json'])
    if not os.path.isfile(filepath):
        return jsonify({"info":"Info about uid='" + uid + "' not found"})
    
    fp = open(filepath)
    info = json.load(fp)

    return jsonify(info)


def uposledzony_pipeline():
    
    dictionary = {}
    
    filepath_img = '/home/michal/repo/road-sign-checker/flask/App/static/photos/6db324da-a096-4872-ba58-b1231f4badc1.jpg'
    filepath_mask = '/home/michal/repo/road-sign-checker/flask/App/static/photos/6db324da-a096-4872-ba58-b1231f4badc1_mask.jpg'
    filepath_json = '/home/michal/repo/road-sign-checker/flask/App/static/info/6db324da-a096-4872-ba58-b1231f4badc1.json'
    mask = ci.getFinalMaskFromImage(filepath_img)
    cv2.imwrite(filepath_mask, mask)
    dictionary['maskShape'] = str(iaf.getMaskShape(mask))
    
    if dictionary['maskShape'] == 'ZnakShape.OCTAGON' or dictionary['maskShape'] == 'ZnakShape.UNKNOWN':
        with open(filepath_json, "w") as outfile:
            json.dump(dictionary, outfile)
        return
        
    dictionary['finalColorClasifaier'] = cc.finalColorClasifaier(ci.readImageAsRGB(filepath_img), mask)
    
    with open(filepath_json, "w") as outfile:
        json.dump(dictionary, outfile)

@app.route('/kurwamac', methods=['GET'])
@limiter.limit("1/second")
def kurwamac():
    thread = Thread(target=uposledzony_pipeline)
    thread.start()
    
    return jsonify({"info":"XDD","uid":0})
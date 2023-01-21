from App import app
from flask import render_template, url_for, redirect, flash, request, session, jsonify
import os
from werkzeug.utils import secure_filename
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from threading import Thread
from time import sleep


limiter = Limiter(get_remote_address,app=app,storage_uri="memory://")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def pipeline():
    sleep(10)
    print('This is from another thread')

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
    
    thread = Thread(target=pipeline)
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
    
    
        

    return jsonify({"uid":uid})




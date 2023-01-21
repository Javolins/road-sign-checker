from flask import Flask, render_template
import flask_cors
from markupsafe import escape

UPLOAD_FOLDER = '/home/michal/repo/road-sign-checker/flask/App/static/photos/'
DOWNLOAD_FOLDER = '/home/michal/repo/road-sign-checker/flask/App/static/info/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

flask_cors.CORS(app, expose_headers='Authorization')

from App import routes
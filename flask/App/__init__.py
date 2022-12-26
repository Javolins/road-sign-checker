from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

from App import routes
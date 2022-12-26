from App import app
from flask import render_template, url_for, redirect, flash

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


import logging

from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for , flash
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from models import Base, InstaImage
from datetime import date, datetime

import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.Model = Base

@app.route('/', methods=['GET'])
def renderIndex(): 
	return render_template('index.html')

@app.route('/fetch/', methods=['GET'])
def fetchImages(): 
	newDate = (datetime.strptime('10/09/1988','%m/%d/%Y'))
	newImage = InstaImage(33333, newDate, "", "", "", "", 666)
	db.session.add(newImage)
	db.session.commit()
	return str(newImage.ID)

import logging

from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for , flash
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from models import Base, InstaImage, Subscription
from datetime import date, datetime
import calendar
import requests
import json
import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.Model = Base

@app.route('/', methods=['GET'])
def renderIndex(): 
	return render_template('index.html')

@app.route('/api/subscriptions/', methods=['GET'])
def returnSecretCode():
	secretCodeArg = 'hub.challenge'
	if not(secretCodeArg in request.args):
		abort(400)
	else:
		secretCodeString = str(request.args[secretCodeArg])
		return secretCodeString

@app.route('/api/subscriptions/', methods=['POST'])
def updateSubscriptionCount():
	jsonData = request.get_json(force=True)
	if(len(jsonData) > 0):
		for update in jsonData:
			if(Subscription.isValidJSON(update)):
				subscriptionID = int(update['subscription_id'])
				matchingSub = db.session.query(Subscription).filter(Subscription.SubID == subscriptionID).first()
				if(not(matchingSub is None)):
					matchingSub.PendingUpdates += 1
					db.session.commit()
				else:
					newSub = Subscription(subscriptionID)
					db.session.add(newSub)
					db.session.commit()
	return jsonify({"RESPONSE":"Success!"})

@app.route('/api/subscriptions/<int:subID>', methods=['GET'])
def getSubscription(subID):
	matchingSub = db.session.query(Subscription).filter(Subscription.SubID == subID).first()
	if(not(matchingSub is None)):
		return jsonify(matchingSub.toJObject())
	else:
		abort(404)

@app.route('/api/subscriptions/<int:subID>', methods=['DELETE'])
def deleteSubscription(subID):
	matchingSub = db.session.query(Subscription).filter(Subscription.SubID == subID).first()
	if(not(matchingSub is None)):
		db.session.delete(matchingSub)
		db.session.commit()
		return jsonify({"RESPONSE":"Success!"})
	else:
		abort(404)
	

@app.route('/api/fetch/', methods=['GET'])
def fetchImages(): 
	#CLIENT ID	edd27e4ca4d440949716ff2938980a79
	#CLIENT SECRET	bcd2a564ee574cdc8f2fb6fe31ab8b34
	clientID = 'edd27e4ca4d440949716ff2938980a79'
	latitude = 30.693365
	longitude = -88.045399
	
	maxTime = ''
	minTime = ''
	latestImage = db.session.query(InstaImage.timeCreated).order_by(InstaImage.timeCreated).first()
	if(not(latestImage is None)):
		minTime = calendar.timegm(latestImage.timeCreated.utctimetuple())
	
	newRequest = requests.get('https://api.instagram.com/v1/media/search?lat='+str(latitude)+'&lng='+str(longitude)+'&client_id='+clientID+'&min_timestamp='+str(minTime))
	requestData = json.loads(newRequest.text)
	
	numberOfNewImages = 0
	#if(requestData and 'data' in requestData):
	#	for each img in data:
			
			
	
	#newDate = (datetime.strptime('02/01/2014','%m/%d/%Y'))
	#newImage = InstaImage(33333, newDate, "", "", "", "", 666)
	#db.session.add(newImage)
	#db.session.commit()
	#return jsonify({"minTime":str(minTime)})
	return jsonify(requestData)

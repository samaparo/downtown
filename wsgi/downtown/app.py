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

app = Flask(__name__, static_folder='../static/', static_url_path='/static')
app.config.from_object(config)

db = SQLAlchemy(app)
db.Model = Base

pageSize = 15
#--- Static Handlers ---
@app.route('/', methods=['GET'])
def renderIndex(): 
	pageOfImages = db.session.query(InstaImage).order_by(InstaImage.timeCreated.desc()).limit(pageSize)
	imageJObjects = []
	for img in pageOfImages:
		imageJObjects.append(img.toJObject())
	return render_template('index.html', images=imageJObjects)

#--- App Endpoints ---
@app.route('/api/images/page/<int:page>', methods=['GET'])
def getLatestImages(page):
	pageOffset = 0
	if page:
		pageOffset = page
	pageOfImages = db.session.query(InstaImage).order_by(InstaImage.timeCreated.desc()).offset(pageSize*pageOffset).limit(pageSize)
	
	imageJObjects = []
	for img in pageOfImages:
		imageJObjects.append(img.toJObject())
	return jsonify({'IMAGES':imageJObjects})


#--- Subscription Endpoints (not used yet) ---
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
	
#--- Fetch Endpoint (called by cron job) --- 
@app.route('/api/fetch/', methods=['GET'])
def fetchImages(): 
	#CLIENT ID	edd27e4ca4d440949716ff2938980a79
	#CLIENT SECRET	bcd2a564ee574cdc8f2fb6fe31ab8b34
	clientID = 'edd27e4ca4d440949716ff2938980a79'
	latitude = 30.693365
	longitude = -88.045399
	
	minTime = 0
	latestImage = db.session.query(InstaImage.timeCreated).order_by(InstaImage.timeCreated.desc()).first()
	if(not(latestImage is None)):
		minTime = calendar.timegm(latestImage.timeCreated.utctimetuple()) + 1
	
	newRequest = requests.get('https://api.instagram.com/v1/media/search?lat='+str(latitude)+'&lng='+str(longitude)+'&client_id='+clientID+'&min_timestamp='+str(minTime))
	requestData = json.loads(newRequest.text)
	
	newImageJSON = []
	if(requestData and 'data' in requestData):
		for img in requestData['data']:
			instaID = img['id']
			timeCreated = datetime.utcfromtimestamp(int(img['created_time']))
			linkURL = img['link']
			captionText =  '' if img['caption'] is None else img['caption']['text']
			mainImageURL = img['images']['standard_resolution']['url']
			thumbImageURL = img['images']['low_resolution']['url']
			creator = int(img['user']['id'])
			newImage = InstaImage(instaID, timeCreated, linkURL, captionText, mainImageURL, thumbImageURL, creator)
			try:
				db.session.add(newImage)
				db.session.commit()	
				newImageJSON.append(newImage.toJObject())
			except:
				pass
			
	return jsonify({'MIN_TIME':datetime.utcfromtimestamp(minTime),'CREATED_IMAGES':newImageJSON})

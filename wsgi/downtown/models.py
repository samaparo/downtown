from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String
from datetime import timedelta
Base = declarative_base()

class InstaImage(Base):
	__tablename__ = 'InstaImage'
	ID = Column(Integer, primary_key = True)
	instaID = Column(String(128), unique=True)
	timeCreated = Column(DateTime)
	linkURL = Column(String(256))
	captionText = Column(String(1024))
	imageURL = Column(String(256))
	thumbnailURL = Column(String(256))
	creatorID = Column(Integer)
	
	def toJObject(self):
		timeCreatedCentral = self.timeCreated - timedelta(hours=6)
		return {'ID': str(self.instaID), 'TIME_CREATED':timeCreatedCentral.strftime('%I:%M %p on %m/%d/%Y '), 'LINK':self.linkURL,'CAPTION':self.captionText,'IMAGE_URL':self.imageURL, 'THUMB_URL':self.thumbnailURL, 'CREATOR':str(self.creatorID)}
		
	def __init__(self, instaID, timeCreated, linkURL, captionText, imageURL, thumbnailURL, creatorID):
		self.instaID = instaID
		self.timeCreated = timeCreated
		self.linkURL = linkURL
		self.captionText = captionText
		self.imageURL = imageURL
		self.thumbnailURL = thumbnailURL
		self.creatorID = creatorID

class Subscription(Base):
	__tablename__ = 'Subscription'
	ID = Column(Integer, primary_key = True)
	SubID = Column(Integer)
	PendingUpdates = Column(Integer)
	
	def __init__(self, SubID):
		self.SubID = SubID
		self.PendingUpdates = 1
	
	def toJObject(self):
		return {"ID":str(self.ID), "SubID":str(self.SubID), "PendingUpdates":str(self.PendingUpdates)}
	
	@staticmethod
	def isValidJSON(jObject):
		return jObject and 'subscription_id' in jObject
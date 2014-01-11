from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String

Base = declarative_base()

class InstaImage(Base):
	__tablename__ = 'InstaImage'
	ID = Column(Integer, primary_key = True)
	instaID = Column(Integer)
	timeCreated = Column(DateTime)
	linkURL = Column(String(256))
	captionText = Column(String(1024))
	imageURL = Column(String(256))
	thumbnailURL = Column(String(256))
	creatorID = Column(Integer)
	
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
		self.PendingUpdates = 0
	
	@staticmethod
	def isValidJSON(jObject):
		return jObject and 'subscription_id' in jObject
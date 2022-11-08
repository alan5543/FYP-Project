# For creating a DB Model
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

# User dB Structure
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    records = db.relationship('Record')


# User Input Record Structure
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    data = db.Column(db.String(100000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#??? the database didnt enter in, CHECK!!!
#??? the UI is messy. LET CORRECT IT
class ExploreNew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))#
    text = db.Column(db.String(100000))
    summary = db.Column(db.String(50000))
    date = db.Column(db.String(50))#
    publish = db.Column(db.String(50))#
    image = db.Column(db.String(1000))
    link = db.Column(db.String(1000))#

# For Cache the Summary Report UX Design
class summaryCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    doc = db.Column(db.String(100000))
    extractKeyWord = db.Column(db.String(100000)) # need to JSONTIFY
    abstractKeyWord = db.Column(db.String(100000)) # need to JSONTIFY
    keyPhase = db.Column(db.String(100000)) # need to JSONTIFY
    extractSum = db.Column(db.String(100000))
    extractSumWordCount = db.Column(db.Integer)
    extractSumSentCount = db.Column(db.Integer)
    abstractSum = db.Column(db.String(100000))
    abstractSumWordCount = db.Column(db.Integer)
    abstractSumSentCount = db.Column(db.Integer)
    coreSent = db.Column(db.String(2000))
    coreSentWordCount = db.Column(db.Integer)
    docWordCount = db.Column(db.Integer)
    docSentWordCount = db.Column(db.Integer)


# For Twitter API Cache UX
class twitterCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String(100))
    foundDate = db.Column(db.String(50))
    data = db.Column(db.String(1000000))
from ast import Constant
from newspaper.configuration import ArticleConfiguration
from pygooglenews import GoogleNews

from newspaper import Article
from website import constants
from .models import ExploreNew
from .constants import TOPIC_LIMIT

from flask import current_app
from . import db

import nltk
nltk.download('punkt')

import random

# a news container for exploring the news today
global newlist
newlist = []
    
class extractNews:
    def __init__(self, id, title, text, summary, date, publish, image, link): 
        self.id = id
        self.title = title 
        self.text = text
        self.summary = summary
        self.date = date
        self.publish = publish
        self.image = image
        self.link = link


def toNewlist(app):
    # transfer the app from main to process the db function
    print(constants.LOG_START_PROCESS)
    google = GoogleNews()
    topnew = google.top_news()
    newID = constants.DEFAULT_NEW_ID
    
    for item in topnew['entries']:
        # initialize the elements of news
        link = item['link']
        title = item['title']
        date = item['published']
        publish = item['source']['title']
        
        try:
            print('try start')
            article = Article(item['link'])
            article.download()
            article.parse()
            nltk.download('punkt')
            article.nlp()

            # add the new elements of newspaper
            text = article.text
            summary = article.summary
            image_loc = article.top_image
            if article.top_image == None or article.top_image == "" or len(article.top_image) == 0:
                # a dummy icon for photo not found
                image_loc = constants.DEFAULT_INPUT_IMAGE
            
            # add news item to list
            newlist.append(extractNews(newID, title, text, summary, date, publish, image_loc, link))

            # add to the database as record
            updateDatabase(title, text, summary, date, publish, image_loc, link, app)

            print(constants.LOG_TRY_END)
            newID = newID + 1
        except:
            print(constants.LOG_TRY_SKIP)
    print(constants.LOG_END_PROCESS)



def updateDatabase(title, text, summary, date, publish, image, link, app):
    #  with-statement to take care of setup and teardown
    with app.app_context():
        print(constants.LOG_DB_FIND)

        # create a temp to check whether the news is stored already
        previous_news = ExploreNew.query.filter_by(title=title).first()
        print(constants.LOG_DB_FINISHED)

        if not previous_news:
            # if it is not previously stored, store it in the database
            print(constants.LOG_DB_STORE)
            arrival_news = ExploreNew(title=title, text=text, summary=summary, date=date, publish=publish, image=image, link=link)
            db.session.add(arrival_news)
            db.session.commit()
            print(constants.LOG_DB_SUCCESS)


def select_news_by_topic(topic):
    google = GoogleNews()
    if topic == constants.TOPIC_WORLD:
        return google.topic_headlines('WORLD', proxies=None, scraping_bee = None)
    elif topic == constants.TOPIC_HK:
        return google.geo_headlines('Hong Kong', proxies=None, scraping_bee = None)
    elif topic == constants.TOPIC_BUSINESS:
        return google.topic_headlines('BUSINESS', proxies=None, scraping_bee = None)
    elif topic == constants.TOPIC_TECH:
        return google.topic_headlines('TECHNOLOGY', proxies=None, scraping_bee = None)
    elif topic == constants.TOPIC_ENTERTAIN:
        return google.topic_headlines('ENTERTAINMENT', proxies=None, scraping_bee = None)
    elif topic == constants.TOPIC_SCIENCE:
        return google.topic_headlines('SCIENCE', proxies=None, scraping_bee = None)
    elif topic == constants.TOPIC_SPORTS:
        return google.topic_headlines('SPORTS', proxies=None, scraping_bee = None)
    elif topic == constants.TOPIC_HEALTH:
        return google.topic_headlines('HEALTH', proxies=None, scraping_bee = None)
    else:
        return google.top_news()


def get_news(topic):
    news = select_news_by_topic(topic)
    newID = constants.DEFAULT_NEW_ID
    res = []
    for item in news['entries']:
        # initialize the elements of news
        link = item['link']
        title = item['title']
        date = item['published']
        publish = item['source']['title']
        
        try:
            article = Article(item['link'])
            article.download()
            article.parse()
            article.nlp()

            # add the new elements of newspaper
            text = article.text
            summary = article.summary
            image_loc = article.top_image
            if article.top_image == None or article.top_image == "" or len(article.top_image) == 0:
                # a dummy icon for photo not found
                image_loc = constants.DEFAULT_INPUT_IMAGE
            
            # add news item to list
            res.append(extractNews(newID, title, text, summary, date, publish, image_loc, link))

            # add to the database as record
            updateDatabase(title, text, summary, date, publish, image_loc, link, current_app)

            # if target the news count leave loop
            if newID >= TOPIC_LIMIT:
                break

            # increment the ID
            newID = newID + 1
        except:
            print(constants.LOG_TRY_SKIP)
    return res


def get_news_from_db():
    dbNews = ExploreNew.query.order_by(ExploreNew.date).all()

    # check dbNews contains null or not
    if len(dbNews) == 0:
        dbNews = get_news(constants.TOPIC_WORLD)

    # random the order each time
    random.shuffle(dbNews)
    
    return dbNews
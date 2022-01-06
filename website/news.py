from newspaper.configuration import ArticleConfiguration
from pygooglenews import GoogleNews
import nltk
from newspaper import Article

from website import constants

from .models import ExploreNew
from . import db


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
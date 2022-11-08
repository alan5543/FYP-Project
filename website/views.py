from nltk import text
from sqlalchemy import true
from werkzeug.wrappers import request
from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from website import constants
from website.auth import login
from flask_login import login_required, current_user
from .models import ExploreNew, Record
from . import db

from flask.json import jsonify
import json

# for the file input
from werkzeug.utils import secure_filename
import os
ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# for the URL extraction
import nltk
from newspaper import Article

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        # Authenticated: Go To Landing Page
        return render_template("homePage.html", boolean = True , user=current_user, InputNow=True)
    else:
        # Not Authenticated: Go To Start Page
        return render_template("startPage.html", boolean = True , user=current_user, InputNow=True)


@views.route('/userInput')
@login_required
def userInput():
    return render_template("extraction.html", boolean = True , user=current_user, InputNow=True)


@views.route('/analyzeText', methods=['GET', 'POST'])
@login_required
def analyzeText():
    if request.method == 'POST':
        # get the news article in which the user has written
        newstext = request.form.get('newstext')
        newstitle = request.form.get('newstitle')

        # error handling for news title
        if newstitle == "" or newstitle == None:
            flash(constants.INPUT_TITLE_ERROR, category='error')
            return render_template('extraction.html', boolean = True, user=current_user, InputNow=True)

        # error handling for news article
        if newstext == "" or newstext == None:
            flash(constants.INPUT_TEXT_ERROR, category='error')
            return render_template('extraction.html', boolean = True, user=current_user, InputNow=True)
    

    # create a temp to check whether the news is stored already
    previous_news = Record.query.filter_by(title=newstitle).first()

    if not previous_news:
        # add the news article and title to the database
        new_article = Record(data=newstext, title=newstitle, user_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
    

    flash(constants.INPUT_SUCCESS, category='success')
    return redirect(url_for('reports.newReport', title=newstitle, doc=newstext))
    #return render_template('extraction.html', boolean = True, user=current_user, newstext=newstext, newstitle=newstitle)


@views.route('/analyzeFile', methods=['GET', 'POST'])
@login_required
def analyzeFile():
    if request.method == "POST":

        try:
            # Extract the news title
            newstitle = request.form.get("newstitle")
            if newstitle == "" or newstitle == None:
                flash(constants.INPUT_TITLE_ERROR, category='error')
                return render_template('extraction.html', boolean = True, user=current_user, InputNow=True)

            # Text file input
            # for secure filenames
            file = request.files['myfile']
            filename = secure_filename(file.filename)

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash(constants.NOT_SELECT_FILE, category='error')
                return redirect(request.url)

            # check whether the file is valid or not
            if not allowed_file(file.filename):
                flash(constants.ONLY_SUPPORT_TEXT, category='error')
                return redirect(request.url)
            else:
                # save a temp file for input read
                from main import app
                full_filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], full_filename))
                print(constants.FILE_SAVED)

                # read the text from file
                file = open(os.path.join(app.config['UPLOAD_FOLDER'], full_filename), "r", encoding="utf-8")
                file_content = file.read().replace("\n", " ")
                file.close()
                newstext = file_content
                print(file_content)

                # delete back the temp file
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], full_filename))

                # create a temp to check whether the news is stored already
                previous_news = Record.query.filter_by(title=newstitle).first()

                if not previous_news:
                    # add the news article and title to the database
                    new_article = Record(data=newstext, title=newstitle, user_id=current_user.id)
                    db.session.add(new_article)
                    db.session.commit()


                # route the passage to the website
                flash(constants.INPUT_SUCCESS, category='success')
                return redirect(url_for('reports.newReport', title=newstitle, doc=newstext))
                # return render_template('extraction.html', boolean = True, user=current_user, newstext=newstext, newstitle=newstitle)
        except:
            flash(constants.FILE_ERROR, category='error')
            return render_template('extraction.html', boolean = True, user=current_user, InputNow=True)


@views.route('/analyzeUrl', methods=['GET', 'POST'])
@login_required
def analyzeUrl():
    if request.method == 'POST':
        try:
            # get the news URL in which the user has written
            NewsUrl = request.form.get('NewsUrl')

            # extract the news article from URL though API
            article = Article(NewsUrl)
            article.download()
            article.parse()
            nltk.download('punkt')
            article.nlp()

            # Error Handling if the extracted text is invalid or empty
            if article.text == "" or article.text == None:
                flash(constants.URL_NO_NEWS, category='error')
                return redirect(request.url)

            # Error Handling if the title is empty
            newstitle = article.title
            newstext = article.text
            if article.title == "" or article.title == None:
                newstitle = constants.URL_NO_TITLE

            # create a temp to check whether the news is stored already
            previous_news = Record.query.filter_by(title=newstitle).first()

            if not previous_news:
                # add the news article and title to the Record database
                new_article = Record(data=article.text, title=newstitle, user_id=current_user.id)
                db.session.add(new_article)
                db.session.commit()


            # add the news element to the News database
            from . import news
            from flask import current_app
            newsSum = article.summary if article.summary != "" else constants.URL_NO_SUM
            newsDate = article.publish_date
            newsPublish = constants.URL_DEFAULT_PUBLISHER
            image_loc = constants.DEFAULT_NEWS_IMAGE
            newsImage = article.top_image if article.top_image != "" else image_loc
            newsLink = NewsUrl
            news.updateDatabase(title=newstitle, text=newstext, summary=newsSum, date=newsDate, publish=newsPublish, image=newsImage, link=newsLink, app=current_app)

            # return the text to frontend
            return redirect(url_for('reports.newReport', title=newstitle, doc=newstext))
            # return render_template('extraction.html', boolean = True, user=current_user, newstext=article.text, newstitle=newstitle)
        except:
            # If the web scraping is denied, return a message
            flash(constants.WEB_SCRAP_DENIED, category='error')
            return render_template('extraction.html', boolean = True, user=current_user, InputNow=True)


@views.route('/explore')
@login_required
def explore():
    # for getting the exploreNews newlist
    # from .news import newlist
    from .news import get_news_from_db
    newlist = get_news_from_db()
    topic = news_label(constants.TOPIC_EXPLORE)
    return render_template("explore.html", boolean = True , user=current_user, newlist=newlist, InputNow=True, topic=topic)


@views.route('/exploreTopic')
@login_required
def exploreTopic():
    try:
        topic = request.args.get('title')
        label = news_label(topic)
        # search the news
        from .news import get_news
        newlist = get_news(topic)
        return render_template("explore.html", boolean = True , user=current_user, newlist=newlist, InputNow=True, topic=label)
    except:
        # for getting the exploreNews newlist
        flash(constants.TOPIC_ERROR, category='error')
        return redirect(url_for('views.explore'))


@views.route('/exploreSubmit', methods=['GET', 'POST'])
@login_required
def exploreSubmit():
    if request.method == 'POST':
        # extract the news title and text
        newTitle = request.form.get('newTitle')
        newText = request.form.get('newText')

        print("newTitle----------" + newTitle)
        print("newText----------" + newText)

        # Error Handling
        if newTitle == "":
            flash(constants.NO_EXPLORE_TITLE, category='error')
            return redirect(url_for('views.explore'))

        if newText == "":
            flash(constants.NO_EXPLORE_TEXT, category='error')
            return redirect(url_for('views.explore'))

        # create a temp to check whether the news is stored already
        previous_news = Record.query.filter_by(title=newTitle).first()
        
        if not previous_news:
            # a thread to the database storage for record
            new_article = Record(data=newText, title=newTitle, user_id=current_user.id)

            db.session.add(new_article)
            db.session.commit()


        # pass parameters to the report dashboard for processing
        return redirect(url_for('reports.newReport', title=newTitle, doc=newText))
    # nothing extracted go back the URL
    return redirect(url_for('views.explore'))


@views.route('/createHashTag', methods=['GET', 'POST'])
@login_required
def createHashTag():
    if request.method == 'POST':
        # extract the news title and text
        hashTag = request.form.get('hashTag')
        print("GET THE HASHTAG: " + hashTag)
        # Error Handling
        if hashTag == "":
            flash(constants.NO_EXPLORE_TITLE, category='error')
            return redirect(url_for('reports.wordNetwork'))
        # route to result page
        print("Going to question page ...")
        return redirect(url_for('reports.question', hashtag=hashTag, directHashtag=False))



@views.route('/createInputHashTag', methods=['GET', 'POST'])
@login_required
def createInputHashTag():
    if request.method == 'POST':
        # extract the news title and text
        hashTag = request.form.get('hashTag')
        print("GET THE HASHTAG: " + hashTag)
        # Error Handling
        if hashTag != "":
            # route to result page
            print("Going to question page ...")
            return redirect(url_for('reports.question', hashtag=hashTag, directHashtag=True))
        else:
            flash(constants.NO_EXPLORE_TITLE, category='error')
            return redirect(url_for("views.inputHashtag"))


@views.route('/inputHashtag')
@login_required
def inputHashtag():
    return render_template("inputHashtag.html", boolean = True , user=current_user, InputNow=True)

@views.route('/yourCorner')
@login_required
def corner():
    return render_template("corner.html", boolean = True , user=current_user, InputNow=True)

@views.route('/history')
@login_required
def history():
    return render_template("history.html", boolean = True , user=current_user, InputNow=True)

@views.route('/recommendation')
@login_required
def recommendation():
    return render_template("history.html", boolean = True , user=current_user, InputNow=True)

@views.route('/discuss')
@login_required
def discuss():
    return render_template("history.html", boolean = True , user=current_user, InputNow=True)

@views.route('/HKToday')
@login_required
def hktoday():
    return render_template("hktoday.html", boolean = True , user=current_user, InputNow=True)

@views.route('/aboutUs')
def aboutus():
    return render_template("aboutUs.html", boolean = True , user=current_user, InputNow=True)


@views.route('/delete-note', methods= ['POST'])
def delete_note():
    record = json.loads(request.data)
    recordId = record['recordId']
    record = Record.query.get(recordId)
    if record:
        if record.user_id == current_user.id:
            db.session.delete(record)
            db.session.commit()
            return jsonify({})

@views.route('/read-note', methods= ['POST'])
def read_note():
    record = json.loads(request.data)
    recordId = record['recordId']
    record = Record.query.get(recordId)
    if record:
        retitle = record.title
        retext = record.data
        print("FOUND: " + retitle)
        message = {'retitle':retitle, 'retext':retext}
        # print(message)
        return jsonify(message)
        
    else:
        return jsonify({})


def news_label(topic):
    if topic == constants.TOPIC_WORLD:
        return constants.TOPIC_LABEL_WORLD
    elif topic == constants.TOPIC_HK:
        return constants.TOPIC_LABEL_HK
    elif topic == constants.TOPIC_BUSINESS:
        return constants.TOPIC_LABEL_BUSINESS
    elif topic == constants.TOPIC_TECH:
        return constants.TOPIC_LABEL_TECH
    elif topic == constants.TOPIC_ENTERTAIN:
        return constants.TOPIC_LABEL_ENTERTAIN
    elif topic == constants.TOPIC_SCIENCE:
        return constants.TOPIC_LABEL_SCIENCE
    elif topic == constants.TOPIC_SPORTS:
        return constants.TOPIC_LABEL_SPORTS
    elif topic == constants.TOPIC_HEALTH:
        return constants.TOPIC_LABEL_HEALTH
    else:
        return constants.TOPIC_LABEL_EXPLORE
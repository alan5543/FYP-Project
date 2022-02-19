from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from flask_login import login_required, current_user
from nltk import text
import json

from sqlalchemy import false, true


from website import constants
from . import engine
import requests

reports = Blueprint('reports', __name__)

class newsNow:
   def __init__(self):
      self._title = constants.DEFAULT_TITLE
      self._doc = constants.DEFAULT_DOC

   def _set_all(self, title, doc):
      self._title = title
      self._doc = doc

   def _get_title(self):
      return self._title

   def _set_title(self, title):
      self._title = title

   def _get_doc(self):
      return self._doc

   def _set_doc(self, doc):
      self._doc = doc
      
Result = newsNow()

@reports.route('/newReport')
@login_required
def newReport():
    title = request.args.get('title')
    doc = request.args.get('doc')
    Result._set_all(title, doc)
    return render_template("dashboard.html", boolean = True , user=current_user, InputNow=False)

@reports.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", boolean = True , user=current_user, InputNow=False)

@reports.route('/summary')
@login_required
def summary():
    try: 
        # extract the processing article
        title = Result._get_title()
        doc = Result._get_doc()

        # extract the news image from database
        print("building news image ...")
        from .models import ExploreNew
        foundNews = ExploreNew.query.filter_by(title=title).first()
        newImage = foundNews.image if foundNews else constants.DEFAULT_INPUT_IMAGE

        # check whether the summary is in cache
        print("Finding Summary Cache ...")
        from .models import summaryCache
        previous_summary = summaryCache.query.filter_by(title=title).first()

        print("Finishing Finding Cache")
        if not previous_summary:
            print("Not Found Summary Cache ...")
            # get the summary API
            res = requests.post('http://127.0.0.1:8001/api/get_summarization', json={"title": title, "doc": doc})
            if res.ok:
                result = res.json()
                return render_template("summary.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc, newImage=newImage, result=result) 
            else:
                flash(constants.INPUT_TEXT_ERROR, category='error')
                return redirect(url_for('reports.newReport', title=title, doc=doc))
        else:
            print("Found Summary Cache ...")
            # get the summary from cache
            cache = previous_summary
            # some parameters load from json to list
            extractKeyWord = json.loads(cache.extractKeyWord)
            abstractKeyWord = json.loads(cache.abstractKeyWord)
            keyPhase = json.loads(cache.keyPhase)

            # import summary report
            from .summarizer import summaryReport
            # get the wordCloud directly
            from .engine import buildWordCloud
            cloud = buildWordCloud(doc)
            # generate summary report
            res = summaryReport()
            res.generateSummary(title, doc, extractKeyWord, abstractKeyWord, keyPhase, cloud, cache.extractSum, 
            cache.extractSumWordCount, cache.extractSumSentCount, cache.abstractSum, cache.abstractSumWordCount, cache.abstractSumSentCount,
            cache.coreSent, cache.coreSentWordCount, cache.docWordCount, cache.docSentWordCount)
            # return to frontend
            result = res.__dict__
            print("-------")
            return render_template("summary.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc, newImage=newImage, result=result)

    except Exception as error:
        flash(error, category='error')
        return redirect(url_for('reports.newReport', title=title, doc=doc))


def toJSON(res):
    return json.dumps(res, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)

    

@reports.route('/sentiment')
@login_required
def sentiment():
    title = Result._get_title()
    doc = Result._get_doc()
    from . import sentiment

    # predict the sentiment
    sentimentClassifier = sentiment.sentimentClassifier(doc)
    # predict the emotion
    res = requests.post('http://127.0.0.1:8001/api/get_emotion', json={"news": [doc]})
    if res.ok:
        result = res.json()
        highProbEmotion = result["HighProba"]
        lowProbEmotion = result["lowProba"]
        return render_template("sentiment.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc,sentimentClassifier=sentimentClassifier, highProbEmotion=highProbEmotion, lowProbEmotion=lowProbEmotion)
    else:
        flash(constants.INPUT_TEXT_ERROR, category='error')
        return redirect(url_for('reports.newReport', title=title, doc=doc))


@reports.route('/discoverMore')
@login_required
def discoverMore():
    title = Result._get_title()
    doc = Result._get_doc()
    res = requests.post('http://127.0.0.1:8001/api/get_name_entity', json={"news": doc})
    if res.ok:
        result = res.json()
        htmlLabel = result["html"]
        nameEntity = result["nameEntity"]
        nameHeaders = engine.get_headers(nameEntity)
        return render_template("nameEntity.html", boolean = True, user=current_user, htmlLabel=htmlLabel, InputNow=False, nameEntity=nameEntity, nameHeaders=nameHeaders)
    else:
        flash(constants.INPUT_TEXT_ERROR, category='error')
        return redirect(url_for('reports.newReport', title=title, doc=doc))



@reports.route('/textAnalysis')
@login_required
def textAnalysis():
    # extract the text article
    title = Result._get_title()
    doc = Result._get_doc()

    # import the text analyzer
    from . import analyzer
    textEngine = analyzer.TextAnalyser(doc)
    textEngine.preprocessText(0, 'n')
    textEngine.totalIndexCalculation()
    textEngine.process_detect_language()
    textEngine.save_dispersion_plot()
    textEngine.calculate_readability_score()
    textEngine.listprocessing()

    print(textEngine.distrPath)

    # percentage for marks
    fleshPercent = textEngine.fleshScore
    gfogPercent = (textEngine.gfogScore/20)*100
    smogPercent = textEngine.smogScore
    uniquewordPercent = (len(textEngine.uniqueWord)/len(textEngine.wordTokens))*100
    longestSentLength = max(textEngine.sentTokens, key=len)
    sentPercent = (int(textEngine.sentAvg)/len(longestSentLength))*100

    # after text analysis, build a word list for table
    word_token_list = textEngine.build_word_token_list()
    sent_token_list = textEngine.build_sent_token_list()

    # POS counter
    pos_counter = textEngine.pos_counter()

    # Content Word Proportion
    content_word_list = textEngine.getContentWords()
    total_word_list = textEngine.getTotalWords()
    (content_word_num, function_word_num) = textEngine.contentWordProportion(content_word_list, total_word_list)

    # return the unique words
    unique_words = textEngine.getContentWords()

    return render_template("textAnalysis.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc, textEngine=textEngine,
    fleshPercent=fleshPercent, gfogPercent=gfogPercent, smogPercent=smogPercent, uniquewordPercent=uniquewordPercent, sentPercent=sentPercent,
    word_token_list=word_token_list, pos_counter=pos_counter, sent_token_list=sent_token_list, content_word_num=content_word_num, function_word_num=function_word_num,
    unique_words=unique_words)


@reports.route('/modelling')
@login_required
def modelling():
    title = Result._get_title()
    doc = Result._get_doc()
    return render_template("modelling.html" , boolean = True , user=current_user, InputNow=False, title=title, doc=doc)


@reports.route('/wordNetwork')
@login_required
def wordNetwork():
    title = Result._get_title()
    doc = Result._get_doc()
    # get the hashtags
    res = requests.post('http://127.0.0.1:8001/api/get_hashtag', json={"title": title, "doc": doc})
    if res.ok:
        result = res.json()
        hashtag = result["hashtag"]
        return render_template("wordNetwork.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc, hashtag=hashtag)
    else:
        flash(constants.INPUT_TEXT_ERROR, category='error')
        return redirect(url_for('reports.newReport', title=title, doc=doc))


@reports.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    print("Going to Question Page ...")
    title = Result._get_title()
    doc = Result._get_doc()

    print("Posting to Question Page ...")
    hashtag = request.args.get('hashtag')
    
    directHashtag = request.args.get('directHashtag')
    print("Direct Hashtag: " + directHashtag)

    if directHashtag == 'True':
        print("Go to Custom Hastag ...")
        return render_template("questionUI.html" , boolean = True , user=current_user, InputNow=True, hashtag=hashtag, title=title)
    else:
        print("Go to Dashboard Hastag ...")
        return render_template("questionUI.html" , boolean = True , user=current_user, InputNow=False, hashtag=hashtag, title=title)


# support
@reports.route('/supportHashtagInfo', methods=['GET', 'POST'])
@login_required
def supportHashtagInfo():
    hashTag = request.args.get('hashTag')
    inputStatus = request.args.get('InputNow')
    InputNow = get_input_status(inputStatus)
    # display
    print("HashTag: " + hashTag)
    print("Input Status: " + inputStatus)
    print("Input Boolean: " + str(InputNow))
    # search the hashtags
    res = requests.post('http://127.0.0.1:8001/api/get_tweets', json={"keyword": hashTag})
    if res.ok:
        result = res.json()
        tweets = result["tweets"]
        hotWords = result["hotWords"]
        tweets_num = result["tweets_num"]
        opinon = result["opinon"]
        timeline = result["timeline"]
        return render_template("hashtagInfo.html" , boolean = True , user=current_user, InputNow=InputNow, support=True, tweets=tweets, hotWords=hotWords, tweets_num=tweets_num, opinon=opinon, timeline=timeline, hashTag=hashTag, hashtagDoc=result)
    else:
        title = Result._get_title()
        doc = Result._get_doc()
        flash(constants.INPUT_TEXT_ERROR, category='error')
        return redirect(url_for('reports.newReport', title=title, doc=doc))


# not support
@reports.route('/notSupportHashtagInfo', methods=['GET', 'POST'])
@login_required
def notSupportHashtagInfo():
    hashTag = request.args.get('hashTag')
    inputStatus = request.args.get('InputNow')
    InputNow = get_input_status(inputStatus)
    # display
    print("HashTag: " + hashTag)
    print("Input Status: " + inputStatus)
    print("Input Boolean: " + str(InputNow))
    # search the hashtags
    res = requests.post('http://127.0.0.1:8001/api/get_tweets', json={"keyword": hashTag})
    if res.ok:
        result = res.json()
        tweets = result["tweets"]
        hotWords = result["hotWords"]
        tweets_num = result["tweets_num"]
        opinon = result["opinon"]
        timeline = result["timeline"]

        return render_template("hashtagInfo.html" , boolean = True , user=current_user, InputNow=InputNow, support=False, tweets=tweets, hotWords=hotWords, tweets_num=tweets_num, opinon=opinon, timeline=timeline, hashTag=hashTag, hashtagDoc=result)
    else:
        title = Result._get_title()
        doc = Result._get_doc()
        flash(constants.INPUT_TEXT_ERROR, category='error')
        return redirect(url_for('reports.newReport', title=title, doc=doc))

# detail hashtag
@reports.route('/detailHashTag', methods=['GET', 'POST'])
@login_required
def detailHashTag():
    try:
        res = request.args.get('res')
        res = res.replace("\n", " ")

        inputStatus = request.args.get('InputNow')
        InputNow = get_input_status(inputStatus)
        # print(res)
        # convert to dict
        import ast
        result = ast.literal_eval(res)

        # get all comments
        all_comments = result["tweets"]
        # print("All Comments: " + str(len(all_comments)))
        support_comments = [comment for comment in all_comments if comment["opinion"] == "Support"]
        unsupport_comments = [comment for comment in all_comments if comment["opinion"] == "Unsupport"]
        no_opinons_comments = [comment for comment in all_comments if comment["opinion"] == "No Opinion"]

        # get countries list
        from .map import getCountryList
        distintCountries = result["countries"]
        countryList = getCountryList(all_comments, distintCountries)

        return render_template("detailHashTag.html" , boolean = True , user=current_user, InputNow=InputNow, result=result, support_comments=support_comments, unsupport_comments=unsupport_comments, no_opinons_comments=no_opinons_comments, countryList=countryList)
        #return render_template("detailHashTag.html" , boolean = True , user=current_user, InputNow=False, support=False, tweets=tweets, hotWords=hotWords, tweets_num=tweets_num, opinon=opinon, timeline=timeline)
    except:
        title = Result._get_title()
        doc = Result._get_doc()
        flash(constants.INPUT_TEXT_ERROR, category='error')
        return redirect(url_for('reports.newReport', title=title, doc=doc))

# get input status
def get_input_status(inputStatus):
    if inputStatus == 'True':
        return True
    else:
        return False
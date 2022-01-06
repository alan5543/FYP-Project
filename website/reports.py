from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from flask_login import login_required, current_user
from nltk import text

from website import constants
from . import engine

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
    # extract the processing article
    title = Result._get_title()
    doc = Result._get_doc()
    doc_word_num = engine.getWordCount(doc)
    doc_word_sent = engine.getSentenceCount(doc)

    # extract the news image from database
    from .models import ExploreNew
    foundNews = ExploreNew.query.filter_by(title=title).first()
    newImage = foundNews.image if foundNews else constants.DEFAULT_INPUT_IMAGE
    print("NEW IMAGE: -------- " + newImage)

    # TF*IDF Key Point
    KEY_NUM = 6
    tf_score = engine.tf_score_process(doc)
    idf_score = engine.idf_score_process(doc)
    tf_idf_score = engine.calculate_TF_IDF(tf_score, idf_score)
    top_keys = engine.get_top_num(tf_idf_score, KEY_NUM)
    top_keys_list = list(top_keys.items())
    top_keys_mean_list = engine.wordMeanExtracter(top_keys_list)

    # Machine Learning Key Point Extraction
    PHASE_NUM = 1
    model_keys = engine.keyword_model_process(doc, PHASE_NUM, KEY_NUM)
    m_keys_list = engine.wordMeanExtracter(model_keys)
    model_keys_list = engine.importancePercentageCalculate(m_keys_list, Phase=False)

    # Machine Learning to Extract the Interesting Phase
    PHASE_NUM = 2
    k_phase_list = engine.keyword_model_diversity(doc, PHASE_NUM, KEY_NUM)
    keys_phase_list = engine.importancePercentageCalculate(k_phase_list, Phase=True)

    # Build a word cloud
    word_cloud_height = 400
    word_cloud_width = 800
    word_cloud_color = True
    word_cloud_filename = constants.DEFAULT_CLOUD_NAME

    engine.save_word_cloud(doc, word_cloud_width, word_cloud_height, word_cloud_color, word_cloud_filename)
    word_cloud_path = engine.get_word_cloud(word_cloud_filename)

    # Extractive Summary
    print("HERE1")
    EXTRACT_NUM = 4
    (extract_sum, extract_sum_word, extract_sum_sent) = engine.extractive_summarizer(doc, EXTRACT_NUM)
    print("HERE2")
    # Abstractive Summary
    (abstract_sum, abstract_sum_word, abstract_sum_sent) = engine.getAbstractiveSum(doc)
    print("HERE3")
    # Core Sentence
    (core_sent, core_word_count) = engine.getCoreSent(doc)

    return render_template("summary.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc, top_keys_mean_list=top_keys_mean_list,model_keys_list=model_keys_list, keys_phase_list=keys_phase_list, newImage=newImage,
    word_cloud_path=word_cloud_path, extract_sum=extract_sum, extract_sum_word=extract_sum_word, extract_sum_sent=extract_sum_sent, abstract_sum=abstract_sum, abstract_sum_word=abstract_sum_word, abstract_sum_sent=abstract_sum_sent,
    core_sent=core_sent, core_word_count=core_word_count, doc_word_num=doc_word_num, doc_word_sent=doc_word_sent)

@reports.route('/sentiment')
@login_required
def sentiment():
    title = Result._get_title()
    doc = Result._get_doc()
    from . import sentiment
    sentimentClassifier = sentiment.sentimentClassifier(doc)
    return render_template("sentiment.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc,sentimentClassifier=sentimentClassifier)

@reports.route('/discoverMore')
@login_required
def discoverMore():
    title = Result._get_title()
    doc = Result._get_doc()
    return render_template("nameEntity.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc)

import threading

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

    #def tableforming():
     #   print("running")
       # textEngine.build_word_token_list()
      #  textEngine.pos_counter()
       # return render_template("textAnalysis.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc, textEngine=textEngine,
       # fleshPercent=fleshPercent, gfogPercent=gfogPercent, smogPercent=smogPercent, uniquewordPercent=uniquewordPercent, sentPercent=sentPercent)

    #print("Thread build")
    #threading.Thread(target=tableforming).start()
    #print("Thread End")

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
    return render_template("modelling.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc)

@reports.route('/wordNetwork')
@login_required
def wordNetwork():
    title = Result._get_title()
    doc = Result._get_doc()
    return render_template("wordNetwork.html", boolean = True , user=current_user, InputNow=False, title=title, doc=doc)

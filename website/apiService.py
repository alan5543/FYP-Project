
from flask import Blueprint, render_template, url_for, request, jsonify, flash
import pandas as pd
from pandas.core.algorithms import isin
from website import constants
import json

# NLP 
import spacy
from spacy import displacy

from website.opinons import opinons
nlp = spacy.load('en_core_web_sm')

# analytical engine
from .engine import generate_summary

apiService = Blueprint('apiService', __name__)

@apiService.route('/api/get_tweetAPI', methods=["GET", "POST"])
def get_tweetAPI():
    try:
        if request.method == "POST":
            content = request.json
            rawtext = content["keyword"]
            from .tweet import search_tweet_api
            print("P1")
            tweetAPI = search_tweet_api(rawtext, 10)
            print("P2")
            print(tweetAPI)
            print("P3")
            res = toJSON(tweetAPI)
            return res
    except Exception:
        return{
            "error": Exception
        }

def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

@apiService.route('/api/get_hashtag', methods=["GET", "POST"])
def get_hashtag():
    try:
        if request.method == "POST":
            content = request.json
            title = content['title']
            doc = content["doc"]

            # check dB cache
            from .models import summaryCache
            cache = summaryCache.query.filter_by(title=title).first()

            # initlize the keys
            extractKeys = []
            abstractKeys = []
            keyPhase = []
            extractHash = []
            abstractHash = []
            phaseHash = []

            if not cache:
                print("Hashtag not cached")
                from .engine import getAllKeys
                (extractKeys, abstractKeys, keyPhase) = getAllKeys(doc)
                print("Finsih Key Extraction ...")
                # extract hashtag
                extractHash = [ item.keyword for item in extractKeys]
                abstractHash = [ item.keyword for item in abstractKeys]
                phaseHash = [ item.keyword for item in keyPhase]
                print("Finsih Key Hashing ...")
            else:
                print("Hashtag is cached")
                extractKeys = json.loads(cache.extractKeyWord)
                abstractKeys = json.loads(cache.abstractKeyWord)
                keyPhase = json.loads(cache.keyPhase)

                # extract hashtag
                extractHash = [ item["keyword"] for item in extractKeys]
                abstractHash = [ item["keyword"] for item in abstractKeys]
                phaseHash = [ item["keyword"] for item in keyPhase]

            # combine hash
            hash = extractHash + abstractHash + phaseHash
            # remove dupliate
            hash = list(dict.fromkeys(hash))
            # randomize the hastag
            import random
            random.shuffle(hash)
            # return hashtag
            return {"hashtag": hash}

        else:
            return {
                "message": constants.NO_SUPPORRT_API
            }
    except:
        return{
            "error": constants.REJECT_TO_API
        }


@apiService.route('/api/get_summarization', methods=["GET", "POST"])
def get_summarization():
    try:
        if request.method == "POST":
            content = request.json
            title = content['title']
            doc = content["doc"]

            # generate summary
            res = generate_summary(title, doc)
            # return
            return res

        else:
            return {
                "message": constants.NO_SUPPORRT_API
            }
    except:
        return{
            "error": constants.REJECT_TO_API
        }


@apiService.route('/api/get_tweets', methods=["GET", "POST"])
def get_tweets():
    try:
        if request.method == "POST":

            content = request.json
            rawtext = content["keyword"]

            demo = True
            if demo:
                from .constants import TWEET_DEMO
                return TWEET_DEMO

            # import the tweet extractor
            from .tweet import tweets_analysis, get_hotWords, create_wordcloud, getDistinctCountries
            (tweets, tweets_table) = tweets_analysis(rawtext)
            hotWords = get_hotWords(tweets_table)
            tweets_num = len(tweets)

            # import opinons builder
            from .opinons import opinons
            opinon = opinons()
            opinon.get_opinons(tweets)

            # import timeline builder
            from .timebuilder import timeline_builder, dataframe_to_time_lst
            timeline = timeline_builder(tweets_table)
            timeline = dataframe_to_time_lst(timeline)

            # get countries list
            countries = getDistinctCountries(tweets_table)

            # wordCloud
            create_wordcloud(tweets_table['CleanText'].values)

            res = {
                "tweets": tweets,
                "hotWords": hotWords,
                "tweets_num": tweets_num,
                "opinon": opinon.__dict__,
                "timeline": timeline,
                "countries": list(countries)
            }
            return res
        else:
            return {
                "message": constants.NO_SUPPORRT_API
            }
    except:
        return {
            "error": constants.REJECT_TO_API
        }
        

@apiService.route('/api/get_emotion', methods=["GET", "POST"])
def get_emotion():
    try:
        if request.method == "POST":
            content = request.json
            rawtext = content["news"]

            # import the model
            from . import emotionModel
            res = emotionModel.get_emotion_predict_res(rawtext)
            return res
        else:
            return {
                "message": constants.NO_SUPPORRT_API
            }
    except:
        return {
            "error": constants.REJECT_TO_API
        }


@apiService.route('/api/get_name_entity', methods=["GET", "POST"])
def get_name_entity():
    try:
        if request.method == "POST":
            content = request.json
            rawtext = content["news"]

            # take out the paragraph
            paragraphs = split_paragraph(rawtext)
            paragraphs = [displacy.render(nlp(r), style='ent') for r in paragraphs]

            docx = nlp(rawtext)

            # extract the list of different name entity
            nlp_name_entity = docx.ents
            name_entity_group = []

            for entity in nlp_name_entity:
                name_entity_group.append((entity.label_, entity.text))


            # put on 2D table
            name_entity_table = pd.DataFrame(name_entity_group, columns=('name entity', 'target'))

            # People including fictional
            PERSON_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'PERSON']['target']
            # Nationalities or religious or political groups
            NORP_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'NORP']['target']
            # Buildings, airports, highways, bridges
            FACILITY_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'FACILITY']['target']
            # Companies and Organization
            ORG_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'ORG']['target']
            # Countries, cities, states
            GPE_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'GPE']['target']
            # Non-GPE locations, mountain, water
            LOC_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'LOC']['target']
            # Objects, vehicles, foods
            PRODUCT_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'PRODUCT']['target']
            
            # Named hurricanes, battles, wars, sports event
            EVENT_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'EVENT']['target']
            # Titles of books and songs
            WORK_OF_ART_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'WORK_OF_ART']['target']
            # Names Documents made into laws
            LAW_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'LAW']['target']
            # LANGUAGE
            LANGUAGE_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'LANGUAGE']['target']
            # DATE
            DATE_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'DATE']['target']
            # TIME
            TIME_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'TIME']['target']

            # PERCENT
            PERCENT_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'PERCENT']['target']
            # MONEY
            MONEY_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'MONEY']['target']
            # Measurements, m or km
            QUANTITY_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'QUANTITY']['target']
            # Order, first, secons
            ORDINAL_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'ORDINAL']['target']
            # Numerical
            CARDINAL_named_entity = name_entity_table.loc[name_entity_table['name entity'] == 'CARDINAL']['target']

            nameEntity = {
                "Famous_Person": list(dict.fromkeys(PERSON_named_entity)), #icon-user Danger
                "Nationalities_and_Political": list(dict.fromkeys(NORP_named_entity)), # Danger
                "Building": list(dict.fromkeys(FACILITY_named_entity)), # icon-picture Primary
                "Organization": list(dict.fromkeys(ORG_named_entity)), #icon-share Primary
                "Countries_and_City": list(dict.fromkeys(GPE_named_entity)), #icon-globe Primary
                "Other_Natural_Places": list(dict.fromkeys(LOC_named_entity)), #icon-picture Primary
                "Products": list(dict.fromkeys(PRODUCT_named_entity)), #icon-rocket Success
                "Events": list(dict.fromkeys(EVENT_named_entity)), #icon-compass Success
                "Books_and_Songs": list(dict.fromkeys(WORK_OF_ART_named_entity)), #icon-music-tone-alt
                "Law_Documents": list(dict.fromkeys(LAW_named_entity)), #icon-book-open Success
                "Language": list(dict.fromkeys(LANGUAGE_named_entity)), #icon-plane Danger
                "Important_Date": list(dict.fromkeys(DATE_named_entity)), #icon-calendar Pink
                "Important_Time": list(dict.fromkeys(TIME_named_entity)), #icon-clock Pink
                "Percentage": list(dict.fromkeys(PERCENT_named_entity)), #icon-bar-chart Cyan
                "Money": list(dict.fromkeys(MONEY_named_entity)), #icon-credit-card Cyan
                "Measurement": list(dict.fromkeys(QUANTITY_named_entity)), #icon-cursor-move Cyan
                "Ordinal_Numbers": list(dict.fromkeys(ORDINAL_named_entity)), #icon-directions Cyan
                "Numerical_Data": list(dict.fromkeys(CARDINAL_named_entity)) #icon-info Cyan
                }

            # remove the null value
            nameEntity = remove_none(nameEntity)
            # html box
            html = { "htmlWord": paragraphs }
            # combine result
            result = {"nameEntity": nameEntity, "html": html}

            return jsonify(** result)
        else:
            return {
                "message": constants.NO_SUPPORRT_API
            }
    except:
        return{
            "error": constants.REJECT_TO_API
        }



def remove_none(obj):
    for key, value in list(obj.items()):
        if len(value) == 0:
            del obj[key]
        elif isinstance(value, dict):
            remove_none(value)
    return obj


def split_paragraph(text):
    import re
    texts = text.split('\r\n')
    texts = list(filter(None, texts))
    texts = [re.sub('\s+',' ',t) for t in texts]
    texts = [t.strip() for t in texts]
    return texts

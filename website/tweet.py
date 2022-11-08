import tweepy
import pandas as pd
import nltk
from .emotionModel import get_emotion_predict_res
from .map import getCountry

# load the environment
import os
from dotenv import load_dotenv
load_dotenv()

# Authentication
consumerKey = os.getenv("CONSUMER_KEY")
consumerSecret = os.getenv("CONSUMER_SECRET")
accessToken = os.getenv("ACCESS_TOKEN")
accessTokenSecret = os.getenv("ACCESS_TOKEN_SECRET")


def connect_twitter():
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)
    return api

# recieve the tweet by keyword/ hashtag
def search_tweet(key_word, number_of_tweets):
    api = connect_twitter()
    tweets = tweepy.Cursor(api.search_tweets, q=key_word, tweet_mode='extended', lang='en', result_type = 'popular').items(number_of_tweets)
    return tweets

# recieve the tweet by keyword/ hashtag
def search_tweet_api(key_word, number_of_tweets):
    import json
    api = connect_twitter()
    searched_tweets = [status._json for status in tweepy.Cursor(api.search_tweets, q=key_word, tweet_mode='extended', lang='en', result_type = 'popular').items(number_of_tweets)]
    json_strings = [json.dumps(json_obj) for json_obj in searched_tweets]
    return json_strings


def create_dataframe(tweets):
    tweets_text_list = []
    tweets_authors_list = []
    tweets_date_list = []
    tweets_loc_list = []
    tweets_url_list = []
    
    for tweet in tweets:
        # tweet
        tweets_text_list.append(tweet.full_text)
        
        # User
        user = '@' + tweet.user.name
        tweets_authors_list.append(user)
        
        # Date
        tweets_date_list.append(tweet.created_at)
        
        # location
        loc = tweet.user.location
        if loc == '':
            tweets_loc_list.append("Not Found")
        else:
            tweets_loc_list.append(loc)
        
        # Url
        tweets_url_list.append("https://twitter.com/twitter/statuses/" + str(tweet.id))
    
    # create 2D table
    df = pd.DataFrame({
        "Tweets": tweets_text_list,
        "Publisher": tweets_authors_list,
        "Release": tweets_date_list,
        "Location": tweets_loc_list,
        "Url": tweets_url_list
    })
    return df


# clean the tweets
def cleanText(text):
    import re
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = re.sub(r':', '', text)
    text = re.sub(r'http\S+', '', text)
    return text

# from sentiment
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def tweet_sentiment(tweets):
    lst = tweets["CleanText"]
    index = 0
    for item in lst:
        score = SentimentIntensityAnalyzer().polarity_scores(item)
        analysis = TextBlob(item)
        tweets.loc[index, 'Neg'] = score['neg']
        tweets.loc[index, 'Pos'] = score['pos']
        tweets.loc[index, 'Neu'] = score['neu']
        tweets.loc[index, 'Com'] = score['compound']
        tweets.loc[index, 'Polarity'] = analysis.sentiment.polarity
        tweets.loc[index, 'Subj'] = analysis.sentiment.subjectivity
        # emotion extract
        emotion_value = get_emotion_predict_res([item])
        emotion_result = emotion_value["HighProba"]
        tweets.loc[index, 'Emotion'] = emotion_result["Emotion"]
        tweets.loc[index, 'Emotion_Score'] = emotion_result["Proba"]
        index += 1
    return tweets

def sentiment_checker (row):
   if row['Polarity'] > 0 :
      return 'Postive'
   if row['Polarity'] < 0:
      return 'Negative'
   if row['Polarity'] == 0:
      return 'Neutral'
   return 'N/A'

def subj_checker(row):
   if row['Subj'] == 0 :
      return 'Objective'
   if row['Subj'] > 0:
      return 'Subjective'
   return 'N/A'

def support_checker(row):
    if row['Subj'] > 0:
        if row['Pos'] > row['Neg']:
            return 'Support'
        elif row['Pos'] < row['Neg']:
            return 'Unsupport'
        else:
            return 'No Opinion'
    else:
        return 'No Opinion'

def tweets_determinator(tweets):
    temp = tweets
    temp['sentiment'] = temp.apply (lambda row: sentiment_checker(row), axis=1)
    temp['expression'] = temp.apply (lambda row: subj_checker(row), axis=1)
    temp['opinion'] = temp.apply (lambda row: support_checker(row), axis=1)
    return temp


# extract the pos, neu, neg, subj, obj list
def extract_tweets_list(table):
    pos = table[table["Polarity"] > 0]
    neg = table[table["Polarity"] < 0]
    neu = table[table["Polarity"] == 0]
    subj = table[table["Subj"] > 0]
    obj = table[table["Subj"] == 0]
    return pos, neg, neu, subj, obj


def percentage(part,whole):
    return 100 * float(part)/float(whole)

def get_values(pos, neg, neu, subj, obj):
    total_num = len(pos) + len(neg) + len(neu)
    pos_percent = percentage(len(pos), total_num)
    neg_percent = percentage(len(neg), total_num)
    neu_percent = percentage(len(neu), total_num)
    subj_percent = percentage(len(subj), total_num)
    obj_percent = percentage(len(obj), total_num)
    return pos_percent, neg_percent, neu_percent, subj_percent, obj_percent


# find out support or not support

def get_subjective_comments(table):
    # find out the subjective comment
    subj_table = table.loc[table['Subj'] > 0]
    # judge positive
    support_table = subj_table.loc[subj_table['Pos'] > subj_table['Neg']]
    # judge negative
    unsupport_table = subj_table.loc[subj_table['Neg'] > subj_table['Pos']]
    return support_table, unsupport_table


# hashtag

# define the stop words
import math
from operator import itemgetter
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# extract the comments list
def extract_comments(tweets_table):
    return tweets_table['Tweets']

# combine the comments from tweets table
def combine_comments(tweets_table):
    comments = tweets_table['Tweets']
    return (' '.join(comments))

# Function to check if the word is present in a sentence list
def check_sent(word, sentences):
    final = [all([w in x for w in word]) for x in sentences] 
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))

# Find total words in the text
def tf_score_process(doc):
    tf_score = {}
    # remove the punctuation
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    total_words = tokenizer.tokenize(doc)
    total_word_length = len(total_words)
    for each_word in total_words:
        each_word = each_word.replace('.', '')
        # remove the stop words
        if each_word not in stop_words:
            if each_word in tf_score:
                # increment the word count
                tf_score[each_word] += 1
            else:
                # initializae the word count
                tf_score[each_word] = 1

    # calculate the appearance percentage of each word
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
    return tf_score

# IDF calculation processing
def idf_score_process(doc, comments):
    # define idf list
    idf_score = {}
    # sentence tokenizing
    total_sentences = comments
    total_words = doc.split()
    total_sent_len = len(total_sentences)

    # idf calculate
    for each_word in total_words:
        each_word = each_word.replace('.','')
        # not in stop words filtering
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1
    # perform a calculation
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())
    return idf_score

# final calculation on a list of TF*IDF
def calculate_TF_IDF(tf_score: dict, idf_score: dict):
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    return tf_idf_score

# return the top n of key words
def get_top_num(tf_idf_score :dict, num:int):
    result = dict(sorted(tf_idf_score.items(), key = itemgetter(1), reverse= True)[:num])
    return result

def get_hotWords(tweets_table):
    # combine the comments
    allComments = combine_comments(tweets_table)
    # extract the comments
    comments = extract_comments(tweets_table)
    # TF
    tf = tf_score_process(allComments)
    # IDF
    idf = idf_score_process(allComments, comments)
    # calculation
    tf_idf_cal = calculate_TF_IDF(tf, idf)
    # filter the key which is longer word
    pairs = tf_idf_cal.items()
    filtered_dictionary = {key: value for key, value in pairs if len(key) > 3}
    
    # get common important word (hashtag)
    words = get_top_num(filtered_dictionary, 5)
    # build a hashtag
    hashword = list(words.keys())
    hashtag = ['#' + item.strip() for item in hashword]
    # return hashtag
    return hashtag


# Build the TimeLine

import pandas as pd
from datetime import datetime, timedelta
pd.options.mode.chained_assignment = None

from datetime import timedelta

def roundTime(time):
    roundTo = 30*60
    dt = time.to_pydatetime()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    result =  dt + timedelta(0,rounding-seconds,-dt.microsecond)
    return result

def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

def timeline_builder(tweets):
    temp = tweets
    # round off the time
    # temp['Release'] = temp["Release"].apply(hour_rounder)
    temp['Release'] = temp["Release"].apply(roundTime)
    # sorting the time
    temp.sort_values(by=['Release'])
    # extract the timeline variable
    time_variable = temp[['Release', 'Polarity', 'Neg', 'Pos']]
    # timeline groupby
    timeline = time_variable.groupby("Release").mean().reset_index()
    return timeline



def tweets_analysis(key):
    tweets = search_tweet(key, 100)
    # create dataframe
    table = create_dataframe(tweets)
    # apply the clean function
    table['CleanText'] = table["Tweets"].apply(cleanText)
    # apply country search
    table['Country'] = table['Location'].apply(getCountry)
    # drop duplicate case
    table.drop_duplicates(inplace = True)
    # sentiment search
    table = tweet_sentiment(table)
    table = tweets_determinator(table)
    # convert to obj list
    tweets_res = dataframe_to_lst(table)
    return tweets_res, table


def getDistinctCountries(tweet_table):
    countries = tweet_table['Country'].unique()
    return countries


def dataframe_to_lst(table):
    res = []
    for index, row in table.iterrows():
        item = {}
        item['Tweets'] = row['Tweets']
        item['Publisher'] = row['Publisher']
        item['Release'] = str(row['Release'])
        item['Location'] = row['Location']
        item['Country'] = row['Country']
        item['Url'] = row['Url']
        item['CleanText'] = row['CleanText']
        item['Neg'] = row['Neg']
        item['Pos'] = row['Pos']
        item['Neu'] = row['Neu']
        item['Com'] = row['Com']
        item['Polarity'] = row['Polarity']
        item['Subj'] = row['Subj']
        item['sentiment'] = row['sentiment']
        item['expression'] = row['expression']
        item['opinion'] = row['opinion']
        item['Emotion'] = row['Emotion']
        item['Emotion_Score'] = row['Emotion_Score']
        res.append(item)

    return res


# word cloud
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import os
from flask import current_app

def create_wordcloud(text):
 mask = np.array(Image.open(os.path.join(current_app.config['TWITTER_FOLDER'], 'twitter.png')))
 stopwords = set(STOPWORDS)
 wc = WordCloud(background_color='white',
 mask = mask,
 max_words=3000,
 stopwords=stopwords,
 repeat=True)
 wc.generate(str(text))
 wc.to_file(os.path.join(current_app.config['TWITTER_FOLDER'], 'tweets.png'))
 print('Word Cloud Saved Successfully')
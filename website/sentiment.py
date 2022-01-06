# sentiment determine
# vectorize the word
from sklearn.feature_extraction.text import TfidfVectorizer
# analysis the similairty
from sklearn.metrics.pairwise import cosine_similarity
# sentiment analaysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# with of the hrlp of nltk
import nltk
from string import punctuation
import re
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# sentiment analysis with TextBlob calculation
from textblob import TextBlob

class sentimentSentence:
    def __init__(self, sent, subject, polar):
        self.sentence = sent
        self.subjectivity = subject
        self.polarity = polar

class sentimentClassifier:
    def __init__(self, doc):
        self.doc = doc
        self.positve = 0
        self.negative = 0
        self.netural = 0
        self.output = "Not Defined"
        self.compoundPercent = 0
        self.compoundValue = 0
        self.overallPolarity = 0
        self.overallSubjectivity = 0

        self.sentList = []
        self.most_polar_sent = "Not Defined"
        self.least_polar_sent = "Not Defined"
        self.most_objective_sent = "Not Defined"
        self.most_subjective_sent = "Not Defined"
        # turn on the engine
        self.determine_sentiment(self.doc)
        self.sentiment_distribution(self.doc)


    def determine_sentiment(self, doc):
        # Change to the lower case
        lower_text = doc.lower()
        # Remove the digit
        lower_nodigit_text = ''.join(word for word in lower_text if not word.isdigit())
        # Remove the stop word
        split_words = lower_nodigit_text.split()
        process_text = ' '.join([word for word in split_words if word not in stop_words])

        # process the sentiment analysis
        sa = SentimentIntensityAnalyzer()
        dd = sa.polarity_scores(text=process_text)
        compound = round((1+dd['compound'])/2, 2)

        # postive: compound >= 0.05
        # neutral: -0.05<compound<0.05
        # Negative: compund <= -0.05
        soutput = self.sentiment_output(dd['compound'])
        
        # output to the value
        self.positve = dd['pos']
        self.negative = dd['neg']
        self.netural = dd['neu']
        self.compoundPercent = dd['compound']
        self.compoundValue = compound
        self.output = soutput

    def sentiment_output(self, compound: float):
        if compound >= 0.05:
            return "Positive"
        if compound <= -0.05:
            return "Negative"
        if compound > -0.05 and compound < 0.05:
            return "Netural"

    def sentiment_distribution(self, doc):
        blob = TextBlob(doc)
        self.overallPolarity = blob.sentiment.polarity
        self.overallSubjectivity = blob.sentiment.subjectivity
        # define the first sentence sentient
        sentence = blob.sentences[0]
        self.most_polar_sent = sentence
        self.least_polar_sent = sentence
        self.most_objective_sent = sentence
        self.most_subjective_sent = sentence
        # input the sentence record first
        self.sentList.append(sentimentSentence(sentence, sentence.sentiment.subjectivity, sentence.sentiment.polarity))
        # for loop to find out the most/least
        for sentence in blob.sentences[1:]:
            # append to the sentence list
            self.sentList.append(sentimentSentence(sentence, sentence.sentiment.subjectivity, sentence.sentiment.polarity))
            # find the most polar sentence
            if self.most_polar_sent.sentiment.polarity < sentence.sentiment.polarity:
                self.most_polar_sent = sentence
            # find the least polar sentence
            if self.least_polar_sent.sentiment.polarity > sentence.sentiment.polarity:
                self.least_polar_sent = sentence
            # find the objective sentence
            if self.most_objective_sent.sentiment.subjectivity > sentence.sentiment.subjectivity:
                self.most_objective_sent = sentence
            # find the subjective sentence
            if self.most_subjective_sent.sentiment.subjectivity < sentence.sentiment.subjectivity:
                self.most_subjective_sent = sentence
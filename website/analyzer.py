from enum import unique
from networkx.algorithms.centrality.dispersion import dispersion
import nltk
import re
from nltk import sent_tokenize, word_tokenize
from nltk import classify
from nltk.corpus import stopwords
from string import punctuation
from nltk.corpus.reader import wordlist

from nltk.sem.logic import Tokens
stopwords_en = stopwords.words('english')

import matplotlib
matplotlib.use('Agg')
from matplotlib import pylab

import spacy
from textstat.textstat import textstatistics,legacy_round

class wordToken:
    def __init__(self, word, freq, pos, stem, lem, unique, difficulty):
        self.word = word
        self.freq = freq
        self.length = len(word)
        self.pos = pos
        self.stem = stem
        self.lem = lem
        self.unique = unique
        self.difficulty = difficulty

question_sent = ['yAnswer', 'whQuestion']
exclam_sent = ['Emphasis']
emotion_sent = ['Emotion']

question_pattern = ["do i", "do you", "what", "who", "is it", "why","would you", "how","is there",
                    "are there", "is it so", "is this true" ,"to know", "is that true", "are we", "am i", 
                   "question is", "tell me more", "can i", "can we", "tell me", "can you explain",
                   "question","answer", "questions", "answers", "ask", "Should we", "Should I"]

helping_verbs = ["is","am","can", "are", "do", "does"]


def set_sent_classifier():
    nltk.download('nps_chat')
    # extract the dataset and class
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    # setting the training set data
    featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    # set up the supervisored classifier
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

class sentToken:
    def __init__(self, sent, diffWordList, sent_classifier:nltk.NaiveBayesClassifier):
        self.sent = sent
        self.wordTokenNum = self.setWordTokenNum(sent)
        self.length = len(sent)
        self.type = self.process_sent_classifier(sent, sent_classifier)
        self.dpercent = self.difficultyCal(self.getWordTokens(sent), diffWordList)

    def setWordTokenNum(self, sent):
        return len(word_tokenize(sent))

    def getWordTokens(self, sent):
        return word_tokenize(sent)

    def difficultyCal(self, normalWords, difficultWords):
        totalLen = len(normalWords)
        list1_as_set = set(normalWords)
        intersection = list1_as_set.intersection(difficultWords)
        intersection_as_list = list(intersection)
        diffWordCount = len(intersection_as_list)
        return (diffWordCount/totalLen)*100


    def sentence_type(self, sent, sent_classifier:nltk.NaiveBayesClassifier):
        # classifier = self.set_sent_classifier()
        classifier = sent_classifier
        sent_type = classifier.classify(dialogue_act_features(sent))
        return sent_type

    def is_question(self, sent, sent_type):
        if sent_type in question_sent:
            return True
        else:
            is_ques = False
            # Pattern Checking
            for pattern in question_pattern:
                is_ques  = pattern in sent
                if is_ques:
                    break
            # mutliple sentence and handle ?
            sentence_arr = sent.split(".")
            for sentence in sentence_arr:
                if len(sentence.strip()):
                    first_word = nltk.word_tokenize(sentence)[0]
                    if sentence.endswith("?") or first_word in helping_verbs:
                        is_ques = True
                        break
            # return false if no question detect
            return is_ques
    
    def is_exclam(self, sent, sent_type):
        if sent_type in exclam_sent:
            return True
        else:
            is_ex = False
            # mutliple sentence and handle !
            sentence_arr = sent.split(".")
            for sentence in sentence_arr:
                if len(sentence.strip()):
                    first_word = nltk.word_tokenize(sentence)[0]
                    if sentence.endswith("?") or first_word in helping_verbs:
                        is_ques = True
                        break
            return is_ex

    def is_emotion(self, sent_type):
        if sent_type in emotion_sent:
            return True
        else:
            return False

    def process_sent_classifier(self, sent, sent_classifier:nltk.NaiveBayesClassifier):
        sent = sent.lower().strip()
        sent_type = self.sentence_type(sent, sent_classifier)
        if self.is_question(sent, sent_type):
            return "Interrogative"
        elif self.is_exclam(sent, sent_type):
            return "Exclamation"
        elif self.is_emotion(sent_type):
            return "Emotion"
        else:
            return "Formal Statement"
    
    def getSentType(self):
        return self.type



class TextAnalyser:
    def __init__(self, doc):
        self.doc = doc
        self.wordTokensWifStopword = []
        self.wordTokens = []
        self.sentTokens = []
        self.language = "Default"
        self.langPercent = "0%"
        self.distrPath = ""

        self.simpsonIndex = 0
        self.entropyIndex = 0
        self.lexicalIndex = 0

        self.fleshScore = 0
        self.fleshLevel = "Default"
        self.fleshGrade = "Default"

        self.gfogScore = 0
        self.readingLevel = "Default"
        self.smogScore = 0

        self.sentAvg = 0
        self.sentVar = 0
        self.uniqueWord = []
        self.commonWord = []

        self.pos_counter_list = []
        self.pos_freq = []
        self.word_token_list = []
        self.difficult_word_list = []
        self.sentence_token_list = []

        self.sent_type_counter = []

    
    def getSentenceTokens(self,doc):
        sentence = sent_tokenize(doc)
        return sentence
    
    def getWordTokens(self,sentenceToken):
        words = []
        for sent in sentenceToken:
            # first process of remove punctuation
            sentence = self.firstRemovePunctuation(sent)
            for word in word_tokenize(sentence):
                words.append(word)
        return words
    
    def lowerCaseRemoveStopwords(self,words):
        single_tokenized_lowered = list(map(str.lower,words))
        stopwords_en = set(stopwords.words('english'))
        words_not_stopword = [word for word in single_tokenized_lowered if word not in stopwords_en]
        return words_not_stopword

    def removePunctuation(self,single_tokenized_lowered):
        stopwords_en = set(stopwords.words('english'))
        stopwords_with_punc = stopwords_en.union(set(punctuation))
        clear_words = [word for word in single_tokenized_lowered if word not in stopwords_with_punc]
        return clear_words

    def getCountfromList(self,lst):
        return len(lst)

    def firstRemovePunctuation(self,text):
        import re
        new_text = re.sub(r'([^\s\w_]|_)+', '', text.strip()) # remove punctuation
        return new_text

    def preprocessText(self, stemmingFlag, lem):
        print("Starting the preprocessing ...")
        # get the doc from input
        inputDoc = self.doc
        # sentence tokenization
        self.sentTokens = self.getSentenceTokens(inputDoc)

        # word tokenization
        self.wordTokens = self.getWordTokens(self.sentTokens)
        # save the word with stopwords
        self.wordTokensWifStopword = self.wordTokens
        # lower case and remove stopwords
        self.wordTokens = self.lowerCaseRemoveStopwords(self.wordTokens)
        # remove punctuation
        self.wordTokens = self.removePunctuation(self.wordTokens)
        # doing stemming/ lemmatization/ normal clear tokens
        from nltk.stem import PorterStemmer
        from nltk.stem import WordNetLemmatizer
        # determine do stem or lem or not
        if stemmingFlag == 1:
            # do stemming and return
            porter = PorterStemmer()
            stem_Tokens = []
            for word in self.wordTokens:
                stem_Tokens.append(porter.stem(word))
            # replace the stemming to word tokens
            self.wordTokens = stem_Tokens
        
        elif stemmingFlag == 2:
            # do lemmatizing and return
            wnl = WordNetLemmatizer()
            lem_Tokens = []
            for word in self.wordTokens:
                # lem = 'v' / 'n' / 'a'
                lem_Tokens.append(wnl.lemmatize(word, lem))
            # replace the lemmizaion to word tokens
            self.wordTokens = lem_Tokens
        else:
            print("Output the normal word tokens")
        print("Finish the preprocessing ...")

    def getUniqueTokens(self,token):
        return set(token)
    
    def getTop10CommonWords(self,token, n=10):
        # get the top n of the common words with frequency
        from collections import Counter
        wordCount = Counter(token)
        return wordCount.most_common()[:n]

    def getFreqWords(self,token):
        from collections import Counter
        wordCount = Counter(token)
        return wordCount.most_common()

    def getMostCommonWordsOnly(self,lst):
        res = []
        for word in lst:
            res.append(word[0])
        return res

    def sentenceLengthAverage(self):
        sentences_count = len(self.sentTokens) #split the text into a list of sentences.
        words_count = len(self.wordTokensWifStopword) #split the input text into a list of separate words
        if(self.sentTokens[sentences_count-1]==""): #if the last value in sentences is an empty string
            average_sentence_length = words_count / sentences_count-1
        else:
            average_sentence_length = words_count / sentences_count
        return average_sentence_length #returning avg length of sentence

    # More variance, More Difference between sentence structure
    def sentenceLengthVariance(self,sent_token):
        values = []
        for word in sent_token:
            stripWord = word.replace(' ', '')
            num = len(stripWord)
            values.append(num)
        import statistics
        return statistics.variance(values)


    def listprocessing(self):
        self.sentAvg = self.sentenceLengthAverage()
        self.sentVar = self.sentenceLengthVariance(self.sentTokens)
        self.uniqueWord = self.getUniqueTokens(self.wordTokens)
        self.commonWord = self.getTop10CommonWords(self.wordTokens)

    # Index Calculation ---------------------------------------------------------------------
    def listtohash(self,tokens):
        from collections import Counter
        wordsCount = Counter(tokens)
        return dict(wordsCount.most_common())

    # less simpson index, more diversity on words structure
    def simpson_diversity(self,hashdata):
        def p(n, N):
            if n ==  0:
                return 0
            else:
                return float(n)/N
        N = sum(hashdata.values())
        return sum(p(n, N)**2 for n in hashdata.values() if n != 0)

    def onlyfreqList(self,tokens):
        from collections import Counter
        wordsCount = Counter(tokens)
        lst = wordsCount.most_common()
        numlst = []
        for word in lst:
            numlst.append(word[1])
        return numlst

    # more entropy, the text is more complex
    def Entropy(self,labels, base=2):
        from scipy import stats
        import pandas as pd
        # probability distribution
        probs = pd.Series(labels).value_counts() / len(labels)
        # calculate Entropy using base
        en = stats.entropy(probs, base=base)
        return en

    # Depend on sentence length and distinct/content words length
    # more lexical diversity, more content words depend on passage
    def lexical_diversity(self,tokens):
        return len(set(tokens))/ len(tokens)

    def totalIndexCalculation(self):
        print("Starting calculating the lexical index")
        # calculate the simpson index
        wordTokens = self.getWordTokens(self.doc)
        wordfreqHash = self.listtohash(wordTokens)
        self.simpsonIndex = self.simpson_diversity(wordfreqHash)
        # calculate the entropy
        wordFreLst = self.onlyfreqList(wordTokens)
        self.entropyIndex = self.Entropy(wordFreLst)
        # calculate the lexical diversity
        self.lexicalIndex = self.lexical_diversity(self.wordTokens)
        print("Finish Lexical Index Calculation")

    # Language Detector --------------------------------------------------------------------

    def top_5_lang(self,lang):
        if lang == 'en':
            return 'English'
        elif lang == 'zh':
            return 'Chinese'
        elif lang == 'hi':
            return 'Hindi'
        elif lang == 'es':
            return 'Spanish'
        elif lang == 'fr':
            return 'French'
        else:
            return lang

    def prob_to_percent(self,prob):
        percent = round(100*prob, 5)
        percentage = str(percent) + "%"
        return percentage

    def process_detect_language(self):
        print("Start detecting language")
        from langdetect import detect_langs
        detector = detect_langs(self.doc)
        self.language = self.top_5_lang(detector[0].lang)
        self.langPercent = self.prob_to_percent(detector[0].prob)
        print("Finish language detection")
        

    # Lexical Distribution Graph ------------------------------------------------------------
    
    def dispersion_plot(self, text, words, ignore_case=False, title="Lexical Dispersion Plot", filename='dispersion_plot.png'):
        text = list(text)
        words.reverse()

        if ignore_case:
            words_to_comp = list(map(str.lower, words))
            text_to_comp = list(map(str.lower, text))
        else:
            words_to_comp = words
            text_to_comp = text

        points = [
            (x, y)
            for x in range(len(text_to_comp))
            for y in range(len(words_to_comp))
            if text_to_comp[x] == words_to_comp[y]
        ]
        if points:
            x, y = list(zip(*points))
        else:
            x = y = ()
        pylab.plot(x, y, "b|", scalex=0.1)
        pylab.yticks(list(range(len(words))), words, color="b")
        pylab.ylim(-1, len(words))
        pylab.title(title)
        pylab.xlabel("Word Offset")
        # pylab.show()
        from flask import current_app
        import os

        image_path = os.path.join(current_app.config['IMG_FOLDER'], filename)
        self.distrPath = image_path.replace("website", "..")
        pylab.savefig(image_path)

    def save_dispersion_plot(self):
        print("Starting plot the dispersion graph")
        from nltk.text import Text
        inaugural_texts = Text(self.wordTokens)
        commonWords = self.getTop10CommonWords(self.wordTokens)
        onlycommonWords = self.getMostCommonWordsOnly(commonWords)
        self.dispersion_plot(text=inaugural_texts, words=onlycommonWords, filename='dispersion2_plot.png')
        print("Finish the dispersion plotting")


    # calculating the reading index ----------------------------------------------------------

    def syllables_count(self, word):
        return textstatistics().syllable_count(word)

    def get_word_count(self):
        return len(self.wordTokensWifStopword)

    def avg_syllables_per_word(self, doc):
        syllable = self.syllables_count(doc)
        words = self.get_word_count()
        ASPW = float(syllable) / float(words)
        return legacy_round(ASPW, 1)

    def get_difficult_words_count(self):
        # find the count of difficult word which syllable >= 2
        difficult_words_set = set()
        for word in self.wordTokens:
            syllable_count = self.syllables_count(word)
            if syllable_count >= 2:
                difficult_words_set.add(word)
        return len(difficult_words_set)

    def get_three_syllable_word_count(self):
        three_syllable_word = set()
        for word in self.wordTokensWifStopword:
            syllable_count = self.syllables_count(word)
            if syllable_count >= 3:
                three_syllable_word.add(word)
        return len(three_syllable_word)



    def calculate_flesch_score(self):
        # Lower Score means More Difficult to read
        doc = self.doc
        print("Average: " + str(self.sentenceLengthAverage()))
        
        FRE = 206.835 - float(1.015 * self.sentenceLengthAverage())-float(84.6 * self.avg_syllables_per_word(doc))
        return legacy_round(FRE, 2)

    def determine_flesch_level(self, score):
        # determine the flesch grade and difficulty
        if score >= 0 and score <= 30:
            self.fleshLevel = "Very Difficult"
            self.fleshGrade = "College Graduate"
        elif score >= 30 and score <=50:
            self.fleshLevel = "Difficult"
            self.fleshGrade = "13th to 16th grade"
        elif score >= 50 and score <=60:
            self.fleshLevel = "Fairly Difficult"
            self.fleshGrade = "10th to 12th grade"
        elif score >= 60 and score <=70:
            self.fleshLevel = "Standard"
            self.fleshGrade = "8th to 9th grade"
        elif score >= 70 and score <=80:
            self.fleshLevel = "Fairly Easy"
            self.fleshGrade = "7th grader"
        elif score >= 80 and score <=90:
            self.fleshLevel = "Easy"
            self.fleshGrade = "6th grader"
        elif score >= 90 and score <=100:
            self.fleshLevel = "Very Easy"
            self.fleshGrade = "5th grader"
        else:
            self.fleshLevel = "Normal Level"
            self.fleshGrade = "Normal Grade"


    def calculate_gunning_fog(self):
        doc = self.doc
        wordCount = self.get_word_count()
        diff_wordCount = self.get_three_syllable_word_count()
        complex_per_words = (diff_wordCount/ wordCount*100)
        finalGrade = 0.4 * (self.sentenceLengthAverage() + complex_per_words)
        return finalGrade

    def determine_gfog(self, score):
        index = int(score)
        if index == 6:
            self.readingLevel = "Sixth grade"
        elif index == 7:
            self.readingLevel = "Seventh grade"
        elif index == 8:
            self.readingLevel = "Eighth grade"
        elif index == 9:
            self.readingLevel = "High school freshman"
        elif index == 10:
            self.readingLevel = "High school sophomore"
        elif index == 11:
            self.readingLevel = "High school junior"
        elif index == 12:
            self.readingLevel = "High school senior"
        elif index == 13:
            self.readingLevel = "College freshman"
        elif index == 14:
            self.readingLevel = "College sophomore"
        elif index == 15:
            self.readingLevel = "College junior"
        elif index == 16:
            self.readingLevel = "College junior"
        elif index >= 17:
            self.readingLevel = "College graduate"
        else:
            self.readingLevel = "Junior"
    
    def calculate_smog_index(self):
        doc = self.doc
        sentence_count = self.getCountfromList(self.sentTokens)
        if sentence_count >= 3:
            mutli_syn_words = self.get_three_syllable_word_count()
            smog_value = (1.043 * (30 * (mutli_syn_words/ sentence_count))**0.5) + 3.1291
            return legacy_round(smog_value, 1)
        else:
            return 0

    def calculate_readability_score(self):
        print("Calculating the readability...")
        # flesh score
        self.fleshScore = self.calculate_flesch_score()
        self.determine_flesch_level(self.fleshScore)
        # gunning fog
        self.gfogScore = self.calculate_gunning_fog()
        self.determine_gfog(self.gfogScore)
        # smog-> dirty word
        self.smogScore = self.calculate_smog_index()
        print("Finishing the readability calculation")

    #--------------------------------------------------------------------------------------
    # Build a word token list
    def build_word_token_list(self):
        word_token_list = []
        import spacy
        nlp = spacy.load("en_core_web_sm")
        
        from nltk.stem import PorterStemmer
        from nltk.stem import WordNetLemmatizer
        porter = PorterStemmer()
        wnl = WordNetLemmatizer()

        # getFreqWords List
        wordList = self.getFreqWords(self.wordTokens)
        for token in wordList:
            word = token[0]
            freq = token[1]

            if not word.isnumeric():

                # import spacy model
                print("Finding POS")
                doc = nlp(word)
                pos_tags = [x.pos_ for x in doc]
                self.pos_counter_list.append(pos_tags[0])

                # import nltk stemming model
                print("Finding Stem")
                stem = porter.stem(word)
                # import nltk lemmization model
                print("Finding Lem")
                lem = wnl.lemmatize(word, 'n')

                uni = "False"
                # whether it is unique
                if word in self.uniqueWord or freq == 1:
                    uni = "True"
                # whether it is difficult word
                diff = "False"
                print("Finding unique difficult")
                syllable_count = self.syllables_count(word)
                if syllable_count >= 3:
                    self.difficult_word_list.append(word)
                    diff = "True"
                # add to the table
                word_token_list.append(wordToken(word, freq, pos_tags, stem, lem, uni, diff))

        return word_token_list
    
    #--------------------------------------------------------------------------------------
    # POS Counter
    def pos_counter(self):
        from collections import Counter
        posCount = Counter(self.pos_counter_list)
        return posCount.most_common()
    
    #--------------------------------------------------------------------------------------
    # Calculate the proportion of content word/ unique word
    def getContentWords(self):
        return self.uniqueWord

    def getTotalWords(self):
        return self.wordTokens

    def contentWordProportion(self, unique_word, total_word):
        content_word = len(unique_word)
        function_word = len(total_word)-len(unique_word)
        return (content_word, function_word)
    
    #--------------------------------------------------------------------------------------
    # Sentence Package

    def set_sent_classifier(self):
        # build a sentence classifier
        nltk.download('nps_chat')
        # extract the dataset and class
        posts = nltk.corpus.nps_chat.xml_posts()[:10000]
        # setting the training set data
        featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
        size = int(len(featuresets) * 0.1)
        train_set, test_set = featuresets[size:], featuresets[:size]
        # set up the supervisored classifier
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        return classifier

    def build_sent_token_list(self):
        index = 1
        # build the supervisored classifier
        sent_classifier = set_sent_classifier()
        sent_type = []
        for sent in self.sentTokens:
            print("LOGGER--------------" + str(index))
            index = index + 1
            sentClassifier = sentToken(sent, self.difficult_word_list, sent_classifier)
            self.sentence_token_list.append(sentClassifier)
            sent_type.append(sentClassifier.getSentType())

        # sentence type counter
        from collections import Counter
        sentCount = Counter(sent_type)
        self.sent_type_counter = sentCount.most_common()
        # return back the sentence token list
        return self.sentence_token_list
    
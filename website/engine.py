#----------------------------------------------------------------------------------------
# ERROR HANDLING
from flask import flash

from website.summarizer import summaryReport
from . import constants

# Key word Extraction Unsupervisored Learning (TF*IDF)
from pickle import STRING
from nltk import tokenize
from operator import itemgetter
import math

# Remove Stopwords
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
stop_words = set(stopwords.words('english'))

# Find total words in the text
def tf_score_process(doc: STRING):
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

# Function to check if the word is present in a sentence list
def check_sent(word, sentences):
    final = [all([w in x for w in word]) for x in sentences] 
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))

# IDF calculation processing
def idf_score_process(doc: STRING):
    # define idf list
    idf_score = {}
    # sentence tokenizing
    total_sentences = tokenize.sent_tokenize(doc)
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

#----------------------------------------------------------------------------------------
# find the definition of Key word
from nltk.corpus import wordnet

class keyMean:
    def __init__(self, keyword, mark, definition):
        self.keyword = keyword
        self.mark = mark
        self.definition = definition

class keyPhase:
    def __init__(self, keyword, mark):
        self.keyword = keyword
        self.mark = mark

def wordMeanExtracter(lst: list):
    keyMeanLst = []
    for keyword in lst:
        word = keyword[0]
        mark = keyword[1]
        try:
            syn = wordnet.synsets(word)
            synMean = syn[0].definition()
            keyMeanLst.append(keyMean(word, mark, synMean))
        except:
            keyMeanLst.append(keyMean(word, mark, constants.DEFAULT_MEANING))
    return keyMeanLst

def importancePercentageCalculate(lst: list, Phase: bool):
    if not Phase:
        keyMeanLst = []
        for kword in lst:
            word = kword.keyword
            mark = kword.mark*100
            definition = kword.definition
            keyMeanLst.append(keyMean(word, mark, definition))
        return keyMeanLst
    else:
        phaseMeanLst = []
        for kword in lst:
            word = kword[0]
            mark = kword[1]*100
            phaseMeanLst.append(keyPhase(word, mark))
        return phaseMeanLst

#----------------------------------------------------------------------------------------
# Key word Extraction Supervisored Learning (Using BERT Semi-supervised Sequence Learning)
from keybert import KeyBERT

# construct and import the model
keyword_model = KeyBERT(model="distilbert-base-nli-mean-tokens")

# keyword model processing
def keyword_model_process(doc: STRING, phase_num: int, top_n: int):
    normal_analysis_list = keyword_model.extract_keywords(
        doc,
        top_n=top_n,
        keyphrase_ngram_range=(1,phase_num),
        stop_words="english"
    )
    # return the keywords list back
    return normal_analysis_list

# keymord model processing more diversity
def keyword_model_diversity(doc: STRING, phase_num: int, top_n: int):
    diversity_analysis_list = keyword_model.extract_keywords(
        doc,
        top_n=top_n, 
        keyphrase_ngram_range=(1, phase_num),
        stop_words = "english",
        use_maxsum=True,
        nr_candidates=20
    )
    # the keywords list return
    return diversity_analysis_list

# the function for only return the keywords without count
def extracted_keywords_list(keywords_list: list):
    returned_list = []
    for item in keywords_list:
        returned_list.append(item[0])
    # return the only-keyword list
    return returned_list

#----------------------------------------------------------------------------------------
# Word Cloud Extraction

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import os
from flask import current_app

def get_word_cloud(img_filename):
    # get the file name of the first file
    #img_file = os.listdir(app.config['IMG_FOLDER'][0])
    
    # recieve the path of img
    image_path = os.path.join(current_app.config['IMG_FOLDER'], img_filename + '.png')
    #full_path = os.path.join(app.config['IMG_FOLDER'], img_file)

    # return the path of img
    print("IMG PATH: " + image_path)
    return image_path

def save_word_cloud(text, cwidth, cheight, darkcolorMode, img_filename):
    # Create a word cloud
    # with height and width and text definiton
    # remove the stopwords
    # cwidth = 800 and cheight = 400

    stopwords = set(STOPWORDS)
    wc = WordCloud(width = cwidth,
                    height = cheight,
                    stopwords = stopwords)

    if darkcolorMode == True:
        # set the color to dark
        wc.background_color = "black"
    else:
        # set to the light color
        wc.background_color = "white"

    # generate the text to cloud
    wc.generate(text=text)

    # set the picture setting
    plt.figure(figsize=(20,10), facecolor='k', edgecolor='k')
    plt.imshow(wc, interpolation='bicubic') 
    plt.axis('off')
    plt.tight_layout()

    print("IMG FOLDER: " + current_app.config['IMG_FOLDER'])

    # create path to save wc image
    image_path = os.path.join(current_app.config['IMG_FOLDER'], img_filename + '.png')

	# Clean previous image from the given path
    CleanCache(directory=current_app.config['IMG_FOLDER'])

	# save the image file to the image path
    plt.savefig(image_path)
    plt.close()
    print("saved wc")


def buildWordCloud(doc):
    # Build a word cloud
    print("Building the cloud ...")
    word_cloud_height = 400
    word_cloud_width = 800
    word_cloud_color = True
    word_cloud_filename = constants.DEFAULT_CLOUD_NAME
    save_word_cloud(doc, word_cloud_width, word_cloud_height, word_cloud_color, word_cloud_filename)
    word_cloud_path = get_word_cloud(word_cloud_filename)
    return word_cloud_path


class CleanCache:
	'''
	this class is responsible to clear any previous image files
	present due to the past searches made.
	'''
	def __init__(self, directory=None):
		self.clean_path = directory
		# only proceed if directory is not empty
		if os.listdir(self.clean_path) != list():
			# iterate over the files and remove each file
			files = os.listdir(self.clean_path)
			for fileName in files:
				print(fileName)
				os.remove(os.path.join(self.clean_path,fileName))
		print("cleaned!")

#----------------------------------------------------------------------------------------
# Extractive Summarizer with Cos Similarity

from nltk.corpus import stopwords
# import the cosine distance to calculate the cosine similarity
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import re

# pre-action to split out the sentences
def preprocess_text(text):
    article = tokenize.sent_tokenize(text)
    sentences = []
    for sentence in article:
        #print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop() 
    #print(sentences)
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the 1st sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the 2nd sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    
    # return the cosine similarity
    return 1 - cosine_distance(vector1, vector2)

# Function to build the cosine similarity matrix
def similarity_matrix_construct(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix

# Return the count of sentences in passage
def getSentenceCount(doc: STRING):
    min1 = len(sent_tokenize(doc))
    min2 = len(re.split(r'[.!?]+', doc))
    number_of_sentences = min(min1, min2)
    return number_of_sentences

# Return the count of words in passage
def getWordCount(doc: STRING):
    res = doc.split()
    return len(res)

# Call for the function of summarizer
def extractive_summarizer(doc: STRING):
    try:
        stop_words = stopwords.words('english')
        summarize_text = []

        # Read text and tokenize
        sentences =  preprocess_text(doc)

        # Generate Similary Martix across sentences
        sentence_similarity_martix = similarity_matrix_construct(sentences, stop_words)

        # Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

        # Define the top sentence extracted (take 50%)
        top_n = round(len(sent_tokenize(doc)) * 0.5)
        print("TOP_N::::::::::::::::::" + str(top_n))

        for i in range(top_n):
            summarize_text.append(" ".join(ranked_sentence[i][1]))
        
        # construct the summary and combine out
        sum_text = " ".join(summarize_text)
        return sum_text, getWordCount(sum_text), getSentenceCount(sum_text)
    except:
        return constants.DEFAULT_ERROR_MESSAGE, getWordCount(constants.DEFAULT_ERROR_MESSAGE), getSentenceCount(constants.DEFAULT_ERROR_MESSAGE)

#----------------------------------------------------------------------------------------
# Text Summarizer with model
from transformers import pipeline, PegasusForConditionalGeneration, PegasusTokenizer
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
import spacy
nlp = spacy.load('en_core_web_sm')

def chunk_sent(doc):
    print("chunking start ...")
    nest = []
    sents = ""
    length = 0
    tokens = nlp(doc)
    sentences = [str(sent).strip() for sent in tokens.sents]
    for sentence in sentences:
        length += len(sentence)
        if length < 1024:
            sents = sents + sentence
        else:
            nest.append(sents)
            sents = ""
            length = 0
    if sents:
        nest.append(sents)
    print("chuncking finished: " + str(len(nest)))

    return nest
    

def getAbstractiveSum(chunk_sent):
    try:
        summaries = []
        index = 0
        for chunk in chunk_sent:
            index += 1
            print("Processing Chunk " + str(index))
            MAX_LENGTH = round(len(word_tokenize(chunk)) * 0.6)
            MIN_LENGTH = round(len(word_tokenize(chunk)) * 0.2)
            print("CHUNK: " + chunk)
            print("MAX_LENGTH: " + str(MAX_LENGTH))
            print("MIN_LENGTH: " + str(MIN_LENGTH))
            summary = summarizer(chunk, max_length=MAX_LENGTH, min_length=MIN_LENGTH, do_sample=False)
            summary_text = summary[0]['summary_text']
            summaries.append(summary_text)
        # combine chunking
        full_summary_text = " ".join(summaries)
        # return report
        return full_summary_text, getWordCount(full_summary_text), getSentenceCount(full_summary_text)

    except:
        return constants.DEFAULT_ERROR_MESSAGE, getWordCount(constants.DEFAULT_ERROR_MESSAGE), getSentenceCount(constants.DEFAULT_ERROR_MESSAGE)
         


#----------------------------------------------------------------------------------------
# Core Sentence Extraction
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

def getCoreSent(doc: STRING):
    tokens = tokenizer(doc, truncation=True, padding="longest", return_tensors="pt")
    print("Starting Generating Core Sentence...")
    summary = model.generate(**tokens)
    print("End Core Extraction...")
    decode_sum = summary[0]
    core_sent = tokenizer.decode(decode_sum)
    return core_sent, getWordCount(core_sent)

#------------------------------------------------------------------------------------------
# Name Recognition Breakdown

def get_headers(obj: dict):
    headers= [k for k in obj.keys()]
    return headers

def get_values(obj: dict):
    values = [k  for  k in  obj.values()]
    return values

def get_couple_list(obj: dict):
    headers = get_headers(obj)
    values = get_values(obj)
    res = []
    pos = 0
    for head in headers:
        for value in values[pos]:
            item = {}
            item[head] = value
            res.append(item)
        pos += 1
    return res


#------------------------------------------------------------------------------------------
# Generate Summary Report

def generate_summary(title, doc):
    # import structure
    from .summarizer import summaryReport
    try:
        # count of the passage
        print("calculating the count of article ...")
        doc_word_num = getWordCount(doc)
        doc_word_sent = getSentenceCount(doc)

        # TF*IDF Key Point
        print ("calculating the TF*IDF")
        KEY_NUM = 6
        tf_score = tf_score_process(doc)
        idf_score = idf_score_process(doc)
        tf_idf_score = calculate_TF_IDF(tf_score, idf_score)
        top_keys = get_top_num(tf_idf_score, KEY_NUM)
        top_keys_list = list(top_keys.items())
        top_keys_mean_list = wordMeanExtracter(top_keys_list)

        # Machine Learning Key Point Extraction
        print("Find the keyword ...")
        PHASE_NUM = 1
        model_keys = keyword_model_process(doc, PHASE_NUM, KEY_NUM)
        m_keys_list = wordMeanExtracter(model_keys)
        model_keys_list = importancePercentageCalculate(m_keys_list, Phase=False)

        # Machine Learning to Extract the Interesting Phase
        print("find the ML keyword ...")
        PHASE_NUM = 2
        k_phase_list = keyword_model_diversity(doc, PHASE_NUM, KEY_NUM)
        keys_phase_list = importancePercentageCalculate(k_phase_list, Phase=True)

        # Build a word cloud
        print("Building the cloud ...")
        word_cloud_height = 400
        word_cloud_width = 800
        word_cloud_color = True
        word_cloud_filename = constants.DEFAULT_CLOUD_NAME

        save_word_cloud(doc, word_cloud_width, word_cloud_height, word_cloud_color, word_cloud_filename)
        word_cloud_path = get_word_cloud(word_cloud_filename)

        # Extractive Summary
        print("Doing the extractive summarization ...")
        (extract_sum, extract_sum_word, extract_sum_sent) = extractive_summarizer(doc)

        # Abstractive Summary
        print("Doing the abstractive Summary ..")
        chunking = chunk_sent(doc)
        (abstract_sum, abstract_sum_word, abstract_sum_sent) = getAbstractiveSum(chunking)
        # (abstract_sum, abstract_sum_word, abstract_sum_sent) = ("No Record", 2, 1)

        # Core Sentence
        print("Extracting the core sentence ...")
        (core_sent, core_word_count) = getCoreSent(doc)
        # (core_sent, core_word_count) = ("No Record", 2)

        # generate struture
        print("Generating the summary report ...")
        res = summaryReport()
        res.generateSummary(title, doc, top_keys_mean_list,model_keys_list, keys_phase_list, word_cloud_path, extract_sum, extract_sum_word, extract_sum_sent,
        abstract_sum, abstract_sum_word, abstract_sum_sent, core_sent, core_word_count, doc_word_num, doc_word_sent)
        
        # store cache to dB
        loadToSummaryCache(res)

        return res.toJSON()

    except Exception as err:
        # res = summaryReport()
        return err

    
def loadToSummaryCache(res: summaryReport):
    print("Summary Cache Start ..")
    from .models import summaryCache
    from . import db
    print("FINSIH IMPOR DB")
    title = res.get_title()
    doc = res.get_doc()
    extractKeyWord = toJSON(res.get_extractKeyWord())
    abstractKeyWord = toJSON(res.get_abstractKeyWord())
    keyPhase = toJSON(res.get_keyPhase())
    extractSum = res.get_extractSum()
    extractSumWordCount = res.get_extractSumWordCount()
    extractSumSentCount = res.get_extractSumSentCount()
    abstractSum = res.get_abstractSum()
    abstractSumWordCount = res.get_abstractSumWordCount()
    abstractSumSentCount = res.get_abstractSumSentCount()
    coreSent = res.get_coreSent()
    coreSentWordCount = res.get_coreSentWordCount()
    docWordCount = res.get_docWordCount()
    docSentWordCount = res.get_docSentWordCount()
    print("FINSIH INSERT DATA")
    # Build the cache
    cache = summaryCache(title=title,doc=doc,extractKeyWord=extractKeyWord,abstractKeyWord=abstractKeyWord, 
    keyPhase=keyPhase,extractSum=extractSum, extractSumWordCount=extractSumWordCount,extractSumSentCount=extractSumSentCount,
    abstractSum=abstractSum,abstractSumWordCount=abstractSumWordCount,abstractSumSentCount=abstractSumSentCount,
    coreSent=coreSent,coreSentWordCount=coreSentWordCount,docWordCount=docWordCount,docSentWordCount=docSentWordCount)
    print("FINISH BUILD THE CACHE")
    print(type(cache))
    print(cache.title)
    if not cache:
        print("The Cache Build is failed")
    else:
        print("Summary Cache start ..")
        # load to dB
        db.session.add(cache)
        db.session.commit()
        print("Summary Cache Success ..")


def toJSON(self):
    import json
    return json.dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)

def getAllKeys(doc):
    # TF*IDF Key Point
    print ("calculating the TF*IDF")
    KEY_NUM = 6
    tf_score = tf_score_process(doc)
    idf_score = idf_score_process(doc)
    tf_idf_score = calculate_TF_IDF(tf_score, idf_score)
    top_keys = get_top_num(tf_idf_score, KEY_NUM)
    top_keys_list = list(top_keys.items())
    top_keys_mean_list = wordMeanExtracter(top_keys_list)
    # Machine Learning Key Point Extraction
    print("Find the keyword ...")
    PHASE_NUM = 1
    model_keys = keyword_model_process(doc, PHASE_NUM, KEY_NUM)
    m_keys_list = wordMeanExtracter(model_keys)
    model_keys_list = importancePercentageCalculate(m_keys_list, Phase=False)
    # Machine Learning to Extract the Interesting Phase
    print("find the ML keyword ...")
    PHASE_NUM = 2
    k_phase_list = keyword_model_diversity(doc, PHASE_NUM, KEY_NUM)
    keys_phase_list = importancePercentageCalculate(k_phase_list, Phase=True)
    # return the keys
    return (top_keys_mean_list, model_keys_list, keys_phase_list)

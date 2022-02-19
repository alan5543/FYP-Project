import json


class summaryReport:
    def __init__(self):
        self.title = "Error"
        self.doc = "Error"
        self.top_keys_mean_list = []
        self.model_keys_list = []
        self.keys_phase_list = []
        self.word_cloud_path = "Error"
        self.extract_sum = "Error"
        self.extract_sum_word = 0
        self.extract_sum_sent = 0
        self.abstract_sum = "Error"
        self.abstract_sum_word = 0
        self.abstract_sum_sent = 0
        self.core_sent = "Error"
        self.core_word_count = 0
        self.doc_word_num = 0
        self.doc_word_sent = 0

    def generateSummary(self, title, doc, top_keys_mean_list, model_keys_list, keys_phase_list, word_cloud_path, extract_sum, 
    extract_sum_word, extract_sum_sent, abstract_sum,abstract_sum_word, abstract_sum_sent, core_sent,
    core_word_count, doc_word_num, doc_word_sent ):

        self.title = title
        self.doc = doc
        self.top_keys_mean_list = top_keys_mean_list
        self.model_keys_list =model_keys_list
        self.keys_phase_list = keys_phase_list
        self.word_cloud_path = word_cloud_path
        self.extract_sum = extract_sum
        self.extract_sum_word = extract_sum_word
        self.extract_sum_sent = extract_sum_sent
        self.abstract_sum = abstract_sum
        self.abstract_sum_word = abstract_sum_word
        self.abstract_sum_sent = abstract_sum_sent
        self.core_sent = core_sent
        self.core_word_count = core_word_count
        self.doc_word_num = doc_word_num
        self.doc_word_sent = doc_word_sent

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def get_title(self):
        return self.title
    
    def get_doc(self):
        return self.doc
    
    def get_extractKeyWord(self):
        return self.top_keys_mean_list
    
    def get_abstractKeyWord(self):
        return self.model_keys_list

    def get_keyPhase(self):
        return self.keys_phase_list

    def get_extractSum(self):
        return self.extract_sum

    def get_extractSumWordCount(self):
        return self.extract_sum_word

    def get_extractSumSentCount(self):
        return self.extract_sum_sent

    def get_abstractSum(self):
        return self.abstract_sum

    def get_abstractSumWordCount(self):
        return self.abstract_sum_word

    def get_abstractSumSentCount(self):
        return self.abstract_sum_sent

    def get_coreSent(self):
        return self.core_sent

    def get_coreSentWordCount(self):
        return self.core_word_count

    def get_docWordCount(self):
        return self.doc_word_num

    def get_docSentWordCount(self):
        return self.doc_word_sent




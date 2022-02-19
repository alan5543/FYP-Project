import json
class opinons:
    def __init__(self):
        self.support = 0
        self.unsuppoprt = 0
        self.no_opinons = 0
        self.positive = 0
        self.neutral = 0
        self.negative = 0
        self.subjective = 0
        self.objective = 0
        self.anger = 0
        self.disgust = 0
        self.fear = 0
        self.joy = 0
        self.neutral = 0
        self.sadness = 0
        self.shame = 0
        self.surprise = 0
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    def get_opinons(self, tweets):
        for tweet in tweets:
            if tweet["opinion"] == "Support":
                self.support += 1
            elif tweet["opinion"] == "Unsupport":
                self.unsuppoprt += 1
            elif tweet["opinion"] == "No Opinion":
                self.no_opinons += 1

            if tweet["sentiment"] == "Postive":
                self.positive += 1
            elif tweet["sentiment"] == "Negative":
                self.negative += 1
            elif tweet["sentiment"] == "Neutral":
                self.neutral += 1

            if tweet["expression"] == "Subjective":
                self.subjective += 1
            elif tweet["expression"] == "Objective":
                self.objective += 1

            if tweet["Emotion"] == "anger":
                self.anger += 1
            elif tweet["Emotion"] == "disgust":
                self.disgust += 1
            elif tweet["Emotion"] == "fear":
                self.fear += 1
            elif tweet["Emotion"] == "joy":
                self.joy += 1
            elif tweet["Emotion"] == "neutral":
                self.neutral += 1
            elif tweet["Emotion"] == "sadness":
                self.sadness += 1
            elif tweet["Emotion"] == "shame":
                self.shame += 1
            elif tweet["Emotion"] == "surprise":
                self.surprise += 1
# Function to check if the word is present in a sentence list
def check_sent(word, sentences):
    final = [all([w in x for w in word]) for x in sentences]
    print(final)
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    print(sent_len)
    return int(len(sent_len))


word = "you"
sentences =["I love you you.", "you"] 

#print(check_sent(word,sentences))

from textblob import TextBlob

doc = 'I never never hate you'

blob = TextBlob(doc)
print(blob.sentiment.polarity)
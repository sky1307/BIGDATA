# Import library

import re
import pickle

###### INTITIAL ##########
threshold =0.5
with open('tfidf.pkl', 'rb') as f:
    tfidf = pickle.load(f)
with open('lda.pkl', 'rb') as f:
    model = pickle.load(f)

#####   PREPROCESSING ########
my_punctuation = '!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@â'

def remove_links(tweet):
    tweet = re.sub(r'http\S+', '', tweet) 
    tweet = re.sub(r'bit.ly/\S+', '', tweet) 
    tweet = tweet.strip('[link]') 
    return tweet
def remove_users(tweet):
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) 
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) 
    return tweet
def remove_punctuation(tweet):
    tweet = re.sub('['+my_punctuation + ']+', ' ', tweet)  
    return tweet
def remove_number(tweet):
    tweet = re.sub('([0-9]+)', '', tweet) 
    return tweet
def remove_emoji(tweet):  
    tweet = re.sub(r"\\[a-z][a-z]?[0-9]+","",tweet)
    return tweet


def preprocess(tweet):
    tweet = remove_links(tweet)
    tweet = remove_number(tweet)
    tweet = remove_users(tweet)
    tweet = remove_emoji(tweet)
    tweet = remove_punctuation(tweet)     
    tweet = tweet.lower().strip()
    tweet = " ".join(tweet.split())
    return tweet   

####### CLASSIFY ######
def classify(text):
    text=preprocess(text)
    inputVector = tfidf.transform([text])
    score = model.transform(inputVector)
    
    for i in range(len(score[0])):
        if score[0][i] > 0.5:
            return i

    return -1




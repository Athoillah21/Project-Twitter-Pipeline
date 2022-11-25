import tweepy
import re
import numpy as np
import pandas as pd
from datetime import datetime, date
from textblob import TextBlob
import os
from better_profanity import profanity

today = date.today()

df = pd.read_csv(f'/home/athoillah/Documents/Local_Twitter_Pipeline/output/Original/{today}_twitter_data_original.csv')
    
# Cleaned tweet
def clean_tweet(tweet):
    if type(tweet) == np.float:
            return ""
    r = tweet.lower()
    r = profanity.censor(r)
    r = re.sub("'", "", r) # This is to avoid removing contractions in english
    r = re.sub("@[A-Za-z0-9_]+","", r)
    r = re.sub("#[A-Za-z0-9_]+","", r)
    r = re.sub(r'http\S+', '', r)
    r = re.sub('[()!?]', ' ', r)
    r = re.sub('\[.*?\]',' ', r)
    r = re.sub("[^a-z0-9]"," ", r)
    r = r.split()
    stopwords = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from"]
    r = [w for w in r if not w in stopwords]
    r = " ".join(word for word in r)
    return r

cleaned = [clean_tweet(tw) for tw in df['text']]

df2 = pd.DataFrame(cleaned)
df2.columns = ['cleaned_tweet']
df['cleaned_tweet']=df2

# Sentiment Analysis
sentiment_objects = [TextBlob(tweet) for tweet in cleaned]
sentiment_values = [tweet.sentiment.polarity for tweet in sentiment_objects]
subjectivity_values = [tweet.sentiment.subjectivity for tweet in sentiment_objects]

df3 = pd.DataFrame(sentiment_values)
df3.columns = ['polarity']
df['polarity']=df3

df4 = pd.DataFrame(subjectivity_values)
df4.columns = ['subjectivity']
df['subjectivity']=df4

df.drop('text', inplace=True, axis=1)

# print(df.head())

# Save dataframe to csv locally
df.to_csv(f'/home/athoillah/Documents/Local_Twitter_Pipeline/output/Refined/{today}_twitter_data.csv', index=False)

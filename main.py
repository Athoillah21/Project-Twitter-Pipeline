# Import Module
import tweepy
import re
import numpy as np
import pandas as pd
from datetime import datetime, date
from textblob import TextBlob
import os
from better_profanity import profanity


def define_tweet():
    # API Key and Token Twitter
    api_key             = 'J7dKwJ6tNZQGFvcBqDbL2kBjA'
    api_secret_key      = 'Sq09CRB0dEhQltAuiW0uquZgf11axzJIvLH58OzgG3IMDp4bfP'

    access_token        = '1351578684285587457-fvnftTGTj6SrCgmrV88FiaTkKvepg7'
    access_token_secret = 'XR7fKqZMbfqImlEAwtIP9VjlPOcgUDRzHIzmDqBiqetx5'

    today = date.today()

    # Authenticate and Get Tweet
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name='@elonmusk',
                                count=1000,
                                include_rts = False,
                                tweet_mode = 'extended')


    # Define What's will store
    tweet_list      = []
    for tweet in tweets:

        if 'retweeted_status' in tweet._json:
                        full_text = tweet._json['retweeted_status']['full_text']
        else:
                        full_text = tweet.full_text

        refined_tweet = {"user" : tweet.user.screen_name,
                        'text' : full_text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : str(tweet.created_at.date())}
        
        tweet_list.append(refined_tweet)


    df = pd.DataFrame(tweet_list)
    df.to_csv(f'twitter_data_original_{today}.csv', index=False)

def cleaned_and_sentiment():

    today = date.today()
      
    df = pd.read_csv(f'twitter_data_original_{today}.csv')
    
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

    # Save dataframe to csv locally
    df.to_csv('twitter_data.csv', index=False)


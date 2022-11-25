import tweepy
import re
import numpy as np
import pandas as pd
from datetime import datetime, date
import os


# API Key and Token Twitter
api_key             = 'J7dKwJ6tNZQGFvcBqDbL2kBjA'
api_secret_key      = 'Sq09CRB0dEhQltAuiW0uquZgf11axzJIvLH58OzgG3IMDp4bfP'

access_token        = '1351578684285587457-fvnftTGTj6SrCgmrV88FiaTkKvepg7'
access_token_secret = 'XR7fKqZMbfqImlEAwtIP9VjlPOcgUDRzHIzmDqBiqetx5'


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
                        'id' : tweet.id,
                        'text' : full_text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : str(tweet.created_at.date())}
        
    tweet_list.append(refined_tweet)


df = pd.DataFrame(tweet_list)
df.to_csv(f'/home/athoillah/Documents/Local_Twitter_Pipeline/output/twitter_data_original.csv', index=False)




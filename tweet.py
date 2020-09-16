from dotenv import load_dotenv
load_dotenv()
import os
import csv
import tweepy
import threading

auth = None
api = None
customer_key = os.environ.get("TWITTER_CUSTOMER_KEY")
consumer_secret = os.environ.get("TWITTER_CUSTOMER_SECRET")    
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

tweets = []

def tweet():
    for tweet_row in tweets:
        last_tweet = None
        for tweet in tweet_row:
            if(last_tweet):
                last_tweet = api.update_status(tweet, last_tweet.id)
            else:
                last_tweet = api.update_status(tweet)

if customer_key and consumer_secret \
    and access_token and access_token_secret:
    auth = tweepy.OAuthHandler(customer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)


    with open('tweets.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                tweets.append(row[2:])
                line_count += 1

    t = threading.Thread(target=tweet)
    t.start()
else:
    print("Twitter token is not set please export the keys as environment variable to access stream mode")


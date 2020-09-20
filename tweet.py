from dotenv import load_dotenv
load_dotenv()
import os
import csv
import tweepy
import threading
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

auth = None
api = None
customer_key = os.environ.get("TWITTER_CUSTOMER_KEY")
consumer_secret = os.environ.get("TWITTER_CUSTOMER_SECRET")    
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
thread = None
tweets = []

class FileWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        print("file changed")
        read_csv("tweets.csv")
        if(thread):
            thread.end()
        create_thread()


def update_file():
    print("upate the csv file")

def create_thread():
    thread = threading.Thread(target=tweet)
    thread.start()

def read_csv(url):
    with open(url) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                tweets.append(row)
                line_count += 1
def tweet():
    for tweet_row in tweets:
        last_tweet = None
        if (tweet_row[1] != "True"):
            print(tweet_row)        
            print(tweet_row[3:])        
            for tweet in tweet_row[3:]:
                if(last_tweet):
                    print("sending thread tweet")
                    last_tweet = api.update_status(tweet, last_tweet.id)
                else:
                    print("sending first tweet")
                    last_tweet = api.update_status(tweet)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileWatcher()
    observer = Observer()
    observer.schedule(event_handler, "tweets.csv", recursive=False)
    observer.start()
    

    if customer_key and consumer_secret \
    and access_token and access_token_secret:
        auth = tweepy.OAuthHandler(customer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        read_csv("tweets.csv")
        create_thread()
    else:
        print("Twitter token is not set please export the keys as environment variable to access stream mode")
    
    observer.join()

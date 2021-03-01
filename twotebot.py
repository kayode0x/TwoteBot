import tweepy
import time
import wikipedia
from pprint import pprint
from PyDictionary import PyDictionary
import requests
print('*** TWOTE BOT STATUS: ACTIVE ***', flush=True)

CONSUMER_KEY = 'enter the consumer key here'
CONSUMER_SECRET = 'enter the consumer secret here'
ACCESS_KEY = 'enter the access key here'
ACCESS_SECRET = 'enter the access secret here'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('*** active and looking for mentions ***', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.

    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)

        if 'hey' in mention.full_text.lower():
            api.update_status('@' + mention.user.screen_name + ' hi there!', mention.id)

        if 'how are you doing?' in mention.full_text.lower():
            api.update_status('@' + mention.user.screen_name + ' Not bad, thanks for asking ', mention.id)

        if "how're you?" in mention.full_text.lower():
            api.update_status('@' + mention.user.screen_name +
                    ' I am well, thanks', mention.id)

        if 'you good?' in mention.full_text.lower():
            api.update_status('@' + mention.user.screen_name +
                    ' Yes I am, thanks', mention.id)

        if "wiki" in mention.full_text.lower():
            print("found a wiki request, searching and replying")
            twt = mention.full_text.lower()
            keyword = "wiki"
            before_keyword, keyword, after_keyword = twt.partition(keyword)
            to_reply = wikipedia.summary(after_keyword, sentences=1)
            api.update_status('@' + mention.user.screen_name + ' ' + to_reply, mention.id)

        if "who created you?" in mention.full_text.lower():
            api.update_status('@' + mention.user.screen_name + ' Kayode Ogunmakinwa - @kayode0x', mention.id)

        if 'dict' in mention.full_text.lower():
            print('found a dictionary request, searching library and replying')
            twt = mention.full_text.lower()
            keyword = "dict"
            before_keyword, keyword, after_keyword = twt.partition(keyword)
            myDict = PyDictionary(after_keyword)
            to_reply = myDict.getMeanings()
            api.update_status('@' + mention.user.screen_name + ' ' + str(to_reply), mention.id)

        if "active?" in mention.full_text.lower():
            twt = mention.full_text.lower()
            to_reply = "Yeah, I'm active"
            api.update_status('@' + mention.user.screen_name + ' ' + to_reply, mention.id)

while True:
        reply_to_tweets()
        time.sleep(3)

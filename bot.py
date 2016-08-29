# based on http://blog.mollywhite.net/twitter-bots-pt2/#createthetwitterapp


import tweepy
import secrets 
import os
from random import randint

TEST_ONLY = True

filename = 'last_id.txt'
user_name = 'hulk_verb_bot'

auth = tweepy.OAuthHandler(secrets.C_KEY, secrets.C_SECRET)  
auth.set_access_token(secrets.A_TOKEN, secrets.A_TOKEN_SECRET)  
api = tweepy.API(auth)  

def ensure_last_id():
    if not os.path.isfile(filename):
        write_last_id(111)
    
def read_last_id():
    ensure_last_id()
    try:
        f = open(filename, 'r')       
        i =  int(f.read())
    except:
        i = 111
    f.close()
    return i
    
def write_last_id(id_):
        f = open(filename, 'w')
        f.write(str(id_))
        f.close()        
        
def get_new_tweet():
    last_id = read_last_id()
    last_tweet = api.user_timeline(user_name, since_id = last_id, count = 1)
    
    if len(last_tweet) == 1:
        write_last_id(last_tweet[0].id)
        return last_tweet[0].text
    else:
        return ''
        
def get_adverb():
    adverbs = 'adverbs.txt'
    with open(adverbs, 'r') as f:
        ls = f.readlines()
        a = ls[randint(0, len(ls) - 1)]
        return a.replace('\n', '')
    
def decorate_tweet(tweet):
    adverb = get_adverb()
    return tweet + ' ' + adverb.upper()
    
def run():
    nt = get_new_tweet()
    if nt:
        decorated_tweet = decorate_tweet(nt)
        print (decorated_tweet)
        if not TEST_ONLY:
            api.update_status(decorated_tweet, in_reply_to_status_id = read_last_id())
    else:
        print ('nothing new')
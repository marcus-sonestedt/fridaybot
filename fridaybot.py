#!/usr/bin/python3

import tweepy
import secrets
import sys
import datetime
import random

ISOFRIDAY = 5 # because standards

def login():
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_secret)
    api = tweepy.API(auth)
    return api

def generate_message():
    with open('messages.txt') as file:
        lines = file.readlines()   

    random.seed(datetime.datetime.utcnow())
    i = random.randrange(start = 0, stop = len(lines))

    return lines[i].strip() + "\n\n#nopushfridays"

def send_friday_tweet():
    api = login()
    msg = generate_message()
    print("Tweeting: " + msg)
    api.update_status(msg)

if __name__ == '__main__':
    api = login()

    if '--tweet' in sys.argv:
        weekday = datetime.datetime.today().isoweekday()
        if weekday == ISOFRIDAY:
            send_friday_tweet()
        else:
            print("It's not Friday today. Push at will.")

    elif '--test-api' in sys.argv:
        print(api.get_user('twitter'))

    elif '--test-generate-tweet' in sys.argv:
        print(generate_message())

    elif '--test-tweet' in sys.argv:
        api = login()
        msg = "Testing at " + str(datetime.datetime.now())
        api.update_status(msg)
    
    else:
        print("No habla")
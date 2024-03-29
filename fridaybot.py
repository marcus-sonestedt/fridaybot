#!/usr/bin/python3
import tweepy
import secrets
import sys
import datetime
import random
import yaml
import os.path

ISOFRIDAY = 5 # because standards
messageDir = os.path.dirname(os.path.realpath(__file__))

def login():
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_secret)
    api = tweepy.API(auth)
    return api

def generate_message():
    with open(os.path.join(messageDir, 'messages.txt')) as file:
        lines = file.readlines()

    random.seed(datetime.datetime.utcnow())
    i = random.randrange(start = 0, stop = len(lines))

    return lines[i].strip() + "\n\n#nopushfridays"

def generate_message_from_yaml():
    with open(os.path.join(messageDir, 'messages.yaml'), 'r', 4096, 'utf-8') as file:
        repo = yaml.safe_load(file)

    random.seed(datetime.datetime.utcnow())
    i = random.randrange(start=0, stop = len(repo['fridays']))

    tweet = repo['fridays'][i]['tweet']

    if type(tweet) is str:
        ret = { 'text': tweet }
    elif type(tweet) is dict:
        ret = tweet
    else:
        raise Exception("I can't handle the " + str(type(tweet)))

    suffix = "\n\n#nopushfridays"

    if len(ret['text']) < 160 - len(suffix):
        ret['text'] += suffix

    return ret

def send_friday_tweet(api):
    msg = generate_message()
    print("Tweeting: " + msg)
    api.update_status(msg)

def send_friday_yaml_tweet(api):
    tweet = generate_message_from_yaml()
    print("Tweeting:\n" + tweet['text'])

    media_ids = None
    if 'image' in tweet:
        media = api.media_upload('images/' + tweet['image'])
        media_ids = [media.media_id]

    api.update_status(tweet['text'], media_ids=media_ids, attachment_url=tweet.get('video'))

def friday(api):
    weekday = datetime.datetime.today().isoweekday()
    if weekday == ISOFRIDAY:
        send_friday_yaml_tweet(api)
    else:
        print("It's not Friday today. Push at will.")
        print("\nLast tweet was:\n");
        print(api.get_user('fridaybot3').status.text)

if __name__ == '__main__':
    api = login()

    if '--tweet' in sys.argv:
        friday(api)

    elif '--test-api' in sys.argv:
        print(api.get_user('twitter'))

    elif '--test-generate-tweet' in sys.argv:
        print(generate_message())

    elif '--test-generate-yaml-tweet' in sys.argv:
        print(generate_message_from_yaml())

    elif '--test-tweet' in sys.argv:
        msg = "Testing at " + str(datetime.datetime.now())
        media = api.media_upload('images/EEiLoSXWsAcnOMt.png')
        print(media)
        api.update_status(msg, media_ids=[media.media_id], attachment_url='https://twitter.com/i/status/1149652994331303936')

    else:
        print("No habla")

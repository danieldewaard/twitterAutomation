#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script will delete all of the tweets in the specified account.
You may need to hit the "more" button on the bottom of your twitter profile
page every now and then as the script runs, this is due to a bug in twitter.
You will need to get a consumer key and consumer secret token to use this
script, you can do so by registering a twitter application at https://dev.twitter.com/apps
@requirements: Python 2.5+, Tweepy (http://pypi.python.org/pypi/tweepy/1.7.1)
@Original_author: Dave Jeffery
@Co-author: John Troon

@modifed by: Daniel de Waard on the 23/2/2019
"""

import tweepy
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def twitter_authentication():

    #twitter credentials and authentication
    auth = tweepy.OAuthHandler(os.getenv("consumer_key"), os.getenv("consumer_secret"))
    auth.set_access_token(os.getenv("access_token"), os.getenv("access_token_secret"))

    api = tweepy.API(auth)
    
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    
    return api

def batch_delete(api):
    api.verify_credentials().screen_name
    for status in tweepy.Cursor(api.user_timeline).items():
       try:
        api.destroy_status(status.id)
        logger.info("Deleted:"+ str(status.id))
       except:
        logger.info("Failed to delete:" + str(status.id))

if __name__ == "__main__":
    
    api = twitter_authentication()
    logger.info("Authenticated as: %s" % api.me().screen_name)
    
    batch_delete(api)
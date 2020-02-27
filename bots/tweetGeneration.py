#twitterAutomation
#Daniel de Waard, 4/2/19

import requests
import json
import os
import logging
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def request_words(word, request_type):
    
    #"meanslike" : ml
    #"synonym" : rel_syn
    #"kindof" : rel_spc
    #"moregeneralthan": rel_gen
    #"adjectivesforword": rel_jjb    
    #"trigger" : rel_trg
    #"rhyme" : rel_rhy   
    #"topics" : topics
    #"often follow" : lc
    response = requests.get("https://api.datamuse.com/words?"+request_type+"="+word+"&md=p")
    response_json = json.loads(response.text)
    
    return response_json

def generate_rhyming_words(word):
    
    words = request_words(word,"rel_rhy")
    rhyme_words = []
    for x in words: 
        if not " " in x["word"]:
            rhyme_words.append(x["word"])
    
    return rhyme_words

def random_word_from_list(words,proportion):
    return words[random.randrange(0,round((len(words)-1)*proportion))]  

def generate_greeting_words():

    words_ml_hello = request_words("hello","ml")
    greeting_words = []
    
    greeting_exclusions = ['patty','pie','farewells','goodby','hug','good-bye','bye-bye','salvation','bow','anyone','pedicure','mum','anyone','breaker','announcer','amy','someone','anybody','somebody','bye','mom','goodbye','hagrid','operator','elise','eleanor','molly','pete','sakes','aha','pai']
    
    for x in words_ml_hello: 
        
        if not x["word"] in greeting_exclusions:
            greeting_words.append(x["word"])

    return greeting_words

def generate_friend_words():
    
    words_ml_friend = request_words("friend","ml")
    friend_words = []
    
    friend_exclusions = ['playdate','sleepover','with','friendship','booster','quaker','date','bloke','jewel','sadik','breed','ipo','siddiq','ami','amis','pore','pai']
    
    for x in words_ml_friend: 
        #extract only the nouns 
        if ('n' in x["tags"]) and not x["word"] in friend_exclusions: 
            friend_words.append(x["word"])

    return friend_words

def main():
    
    class tweet_structure:
        
        def __init__(tweet):
            tweet.greeting_flag = 0
            tweet.rhyme_flag = 0
            tweet.friend_flag = 0
            tweet.number_of_rhymes = 0
            tweet.greeting_word = ""
            tweet.rhyme_word_1 = ""
            tweet.friend_word = ""
            tweet.tweet_string = "" 
        
        def define_structure(tweet):
            
            if random.randrange(0,10) <= 7:
                tweet.greeting_flag = 1
            
                if random.randrange(0,10) <= 4:
                    tweet.rhyme_flag = 1
                    
            if random.randrange(0,10) <= 6:
                tweet.friend_flag = 1
                
        def create_tweet(tweet):
            
            if tweet.greeting_flag == 1:
                greeting_words = generate_greeting_words()
                tweet.greeting_word = random_word_from_list(greeting_words,1)
            
            if tweet.friend_flag == 1:
                friend_words = generate_friend_words()
                tweet.friend_word = random_word_from_list(friend_words,1)
                
            if tweet.rhyme_flag == 1: 
                rhymes = generate_rhyming_words(tweet.greeting_word)

                if len(rhymes) > 10:
                
                    tweet.rhyme_word_1 = random_word_from_list(rhymes,0.5) 
                    
            string = (tweet.greeting_word + " " + tweet.rhyme_word_1 + " " + tweet.friend_word).strip().capitalize() 
            
            tweet.tweet_string = ' '.join(string.split()).replace(" ", ", ")
            
    for x in range(0, 50):  
        tweet1 = tweet_structure()
        tweet1.define_structure()
        tweet1.create_tweet()
        logger.info(tweet1.tweet_string)
    
if __name__ == "__main__":
    main()
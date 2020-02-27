#twitterAutomation
#Daniel de Waard, 4/2/19

import requests
import json
import os
import logging
import time
import random

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
        rhyme_words.append(x["word"])
    
    return rhyme_words
            
def generate_greeting_words():
    
    words_ml_friend = request_words("friend","ml")
    friend_words = []
    
    friend_exclusions = ['playdate','sleepover','with','friendship','booster','quaker','date']
    
    for x in words_ml_friend: 
        #extract only the nouns 
        if ('n' in x["tags"]) and not x["word"] in friend_exclusions: 
            friend_words.append(x["word"])

    words_ml_hello = request_words("hello","ml")
    greeting_words = []
    
    greeting_exclusions = ['farewells','goodby','hug','good-bye','bye-bye','salvation','bow','anyone','pedicure','mum','anyone','breaker','announcer','amy','someone','anybody','somebody','bye','mom','goodbye','hagrid','operator','elise','eleanor','molly','pete']
    
    for x in words_ml_hello: 
        
        if not x["word"] in greeting_exclusions:
            greeting_words.append(x["word"])
        
    random_greeting = greeting_words[random.randrange(0,round((len(greeting_words)-1)))]   
    random_friend_word = friend_words[random.randrange(0,round((len(friend_words)-1)*0.8))]  

    return greeting_words, friend_words

def main():
    
    [greeting_words, friend_words] = generate_greeting_words()
    
    
    for y in range(0,15):
        random_greeting = greeting_words[random.randrange(0,round((len(greeting_words)-1)))] 
        rhyme = generate_rhyming_words(random_greeting)
        random_friend_word = friend_words[random.randrange(0,round((len(friend_words)-1)))]  
        #print(rhyme)
        print(len(rhyme))
        if len(rhyme) > 10:
            random_rhyme1 = rhyme[random.randrange(0,round((len(rhyme)-1)*0.8))] 
            random_rhyme2 = rhyme[random.randrange(0,round((len(rhyme)-1)*0.8))] 
            
            while random_rhyme1 == random_rhyme2:
                random_rhyme2 = rhyme[random.randrange(0,round((len(rhyme)-1)*0.8))] 
            
            print(random_greeting+", "+random_rhyme1+", "+random_rhyme2+", "+random_friend_word+"!")
        
        else: 
            print(random_greeting+", "+random_friend_word+"!")

            

if __name__ == "__main__":
    main()
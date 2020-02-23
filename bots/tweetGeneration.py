#twitterAutomation
#Daniel de Waard, 4/2/19

import requests
import json
import os
import logging
import time
import random

rain_flag = 1

def request_words(word, request_type):
    
    "meanslike" : ml
        
    "synonym" : rel_syn
        
    "kindof" : rel_spc
        
    "moregeneralthan": rel_gen
        
    "adjectivesforword": rel_jjb    
    
    "trigger" : rel_trg
    
    "rhyme" : rel_rhy
        
    "topics" : topics
    
    response = requests.get("https://api.datamuse.com/words?ml=friend&md=p")

def main():
    
    response = requests.get("https://api.datamuse.com/words?ml=friend")
    
    friend_words = []
    
    response = json.loads(response.text)
    for x in response: 
        friend_words.append(x["word"])
        
    response = requests.get("https://api.datamuse.com/words?ml=hello")

    greeting_words = []

    response = json.loads(response.text)
    for x in response: 
        greeting_words.append(x["word"])
    
    print((len(greeting_words)-1)*0.8*(len(friend_words)-1)*0.8)
    
    for y in range(0,1000):
        
        random_greeting = greeting_words[random.randrange(0,round((len(greeting_words)-1)*0.8))]   

        random_friend_word = friend_words[random.randrange(0,round((len(friend_words)-1)*0.8))]  

        print(random_greeting+", "+random_friend_word+"!")

if __name__ == "__main__":
    main()
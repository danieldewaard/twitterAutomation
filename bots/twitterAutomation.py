#twitterAutomation
#Daniel de Waard, 4/2/19

import tweepy
import requests
import json
import os
import logging
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
i = 0

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

def load_memes():
    
    logger.info("Loading memes")
    
    basepath = "../photos/memes/modified/"
    memes = []
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file():
                #print(entry.name)
                memes.append(entry.name)
    
    logger.info(str(len(memes))+" memes loaded")
    
    return memes

def timing_function(rain_flag):
    
    global time_since_no_rain_post
    global last_no_rain_post
    global time_since_rain_post
    global last_rain_post
    global i
    
    if i == 1:
            last_rain_post = time.time()
            last_no_rain_post = time.time()
            logger.info("Timing: time since last posts all set to 0")
            return 1
    
    if rain_flag == 1:     
        
        time_since_rain_post = time.time() - last_rain_post 
                
        logger.info(last_rain_post)
        logger.info(time_since_rain_post)
        
        if time_since_rain_post >= 3600:
            last_rain_post = time.time()
            return 1
        else: 
            return 0
        
    if rain_flag == 0: 
            
        time_since_no_rain_post = time.time() - last_no_rain_post 
        
        logger.info(last_no_rain_post)
        logger.info(time_since_no_rain_post)
        
        if time_since_no_rain_post >= 21600:
            last_no_rain_post = time.time()
            return 1
        else: 
            return 0


def twitter_automation(api, memes):
    
    global i

    i = i + 1
    
    logger.info(i)
    
    #sourcing the weather
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Taipei&units=metric&appid="+os.getenv("weatherAPI_key"))
    response = json.loads(response.text)
    weather = response["weather"][0]["main"]
    weather_detailed = (response["weather"][0]["description"]).lower()
    temperature = str(round(response["main"]["temp"],1))

    logger.info("Weather successfully obtained!\nCurrent weather: " +weather+"\nDetailed weather: " + weather_detailed+"\nTemperature: "+ temperature)

    weather_detailed_words = weather_detailed.split()

    if ("rain" or "drizzle") in weather_detailed_words:
        rain_flag = 1
        rain_status = "It is raining in Taipei!!"
        rain_hashtag = "#rain"
    else: 
        rain_flag = 0
        rain_status = "It is not raining in Taipei..."
        rain_hashtag = "#norain"

    logger.info("rain status: "+str(rain_flag))    
    
    time_flag = timing_function(rain_flag)
    
    if time_flag == 1: 

        should_meme_be_posted = random.randrange(0,10)
        
        if rain_flag == 0:
            should_meme_be_posted = 10
        
        if should_meme_be_posted >2:

            #updating the twitter status no meme    
            try:
                status = api.update_status(rain_status + "\nCurrent temperature: "+temperature+" degrees \nCurrent weather: "+weather_detailed+" \n#Taipei #Taiwan #weather " + rain_hashtag)
                
                logger.info("Tweet posted. "+rain_status)
                
            except Exception as e:
                
                logger.error("Error posting tweet", exc_info=True)
                raise e
            
        if should_meme_be_posted <=2:
            
            max_memes_address = len(memes)-1
            rand_meme = random.randrange(0,max_memes_address)
            
            #updating the twitter status with a meme    
            try:
                status = api.update_with_media("../photos/memes/modified/"+memes[rand_meme],rain_status + "\nCurrent temperature: "+temperature+" degrees \nCurrent weather: "+weather_detailed+" \n#Taipei #Taiwan #weather " + rain_hashtag +" #memes")
                
                logger.info("Tweet posted. "+rain_status+" A meme was also posted")
                
            except Exception as e:
                
                logger.error("Error posting tweet", exc_info=True)
                raise e
            
    if time_flag == 0: 
        logger.info("Timing constraint: no post made")
        
def main():
    
    api = twitter_authentication()
    
    memes = load_memes()
    
    while True:
        twitter_automation(api,memes)
        time.sleep(600)
        
if __name__ == "__main__":
    main()
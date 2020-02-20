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

def twitter_automation(api): 
    
    global i
    i = i + 1
    
    #sourcing the weather
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Taipei&units=metric&appid="+os.getenv("weatherAPI_key"))
    response = json.loads(response.text)
    weather = response["weather"][0]["main"]
    weather_detailed = (response["weather"][0]["description"]).lower()
    temperature = str(round(response["main"]["temp"],1))

    logger.info("Weather successfully obtained!\nCurrent weather: " + weather+ "\nDetailed weather: " + weather_detailed+"\nTemperature: "+ temperature)

    weather_detailed_words = weather_detailed.split()

    if "rain" in weather_detailed_words:
        rain_flag = 1
        rain_status = "It is raining in Taipei!!"
        rain_hashtag = "#rain"
    else: 
        rain_flag = 0
        rain_status = "It is not raining in Taipei..."
        rain_hashtag = "#norain"

    logger.info("rain status: "+str(rain_flag))    
    
    if rain_flag == 0:
    
        #updating the twitter status    
        try:
            status = api.update_status(rain_status + "\nCurrent temperature: "+temperature+" degrees \nCurrent weather: "+weather_detailed+" \n#Taipei #Taiwan #weather " + rain_hashtag)
            logger.info("Tweet posted, it is not raining")
        except Exception as e:
            logger.error("Error posting tweet", exc_info=True)
            raise e
            
    if rain_flag == 1: 
        
        memes = load_memes()
        
        max_memes_address = len(memes)-1
        rand_meme = random.randrange(0,max_memes_address)
        
        #updating the twitter status    
        try:
            status = api.update_with_media("../photos/memes/modified/"+memes[rand_meme],rain_status + "\nCurrent temperature: "+temperature+" degrees \nCurrent weather: "+weather_detailed+" \n#Taipei #Taiwan #weather " + rain_hashtag +" #memes")
            logger.info("Tweet posted, it is raining and a meme was also posted")
        except Exception as e:
            logger.error("Error posting tweet", exc_info=True)
            raise e
    
def main():
    
    api = twitter_authentication()
    
    while True:
        twitter_automation(api)
        time.sleep(3600)
        
if __name__ == "__main__":
    main()
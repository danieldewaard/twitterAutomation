#twitterAutomation
#Daniel de Waard, 4/2/19

import tweepy
import requests
import json
import os
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#twitter credentials and authentication

auth = tweepy.OAuthHandler(os.getenv("consumer_key"), os.getenv("consumer_secret"))
auth.set_access_token(os.getenv("access_token"), os.getenv("access_token_secret"))

api = tweepy.API(auth)

#sourcing the weather


i = 1

def do_automation(): 
    global i
    i = i + 1
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Taipei&units=metric&appid="+os.getenv("weatherAPI_key"))
    response = json.loads(response.text)

    weather = response["weather"][0]["main"]
    weather_detailed = (response["weather"][0]["description"]).lower()
    temperature = str(response["main"]["temp"])

    print(weather)
    print(weather_detailed)
    print(temperature)

    weather_detailed_words = weather_detailed.split()

    print(weather_detailed_words)

    if "rain" in weather_detailed_words:
        rain_flag = 1
        rain_status = "It is raining in Taipei!!"
        rain_hashtag = "#rain"
    else: 
        rain_flag = 0
        rain_status = "It is not raining in Taipei..."
        rain_hashtag = "#norain"

    print("rain flag: "+str(rain_flag))    

    #updating the twitter status    

    status = api.update_status(str(i)+ rain_status + "\nCurrent temperature: "+temperature+" degrees \nCurrent weather: "+weather_detailed+" \n#Taipei #Taiwan #Weather " + rain_hashtag)

    print(status.text)
    
def main():
    while True:
        do_automation()
        time.sleep(10)
        
if __name__ == "__main__":
    main()
import requests, os
from dotenv import load_dotenv

load_dotenv()

STEAM_HISTORY_URL = "https://steamcommunity.com/market/pricehistory/"
MYKEL_URL='https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json'

params = {
    "country": "US",
    "currency": "3",
    "appid": "730",
}

cookies = {
    "steamLoginSecure": os.getenv("STEAM_LOGIN_SECURE")
}

# Function to fetch from MYKEL's API endpoint for images
def fetchImage(item):
    img=None
    
    res=requests.get(MYKEL_URL)
    data=res.json()
    
    for skin in data:
        if(item in skin['name']):
            img=skin['image']
    return img

# Function to get latest Steam listing price for a given item
def fetchLatestPrice(item_hash_name):
    price=0
    params['market_hash_name']=item_hash_name
    
    res=requests.get(STEAM_HISTORY_URL, params=params, cookies=cookies)
    data=res.json()

    #Get latest listing
    price=data['prices'][-1]
    
    #Get sale value of latest listing
    return price[1]
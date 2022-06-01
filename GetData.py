import os
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from bs4 import BeautifulSoup, Tag

load_dotenv()

#Building variables
api_key = os.getenv("API_KEY")
service_name = 'youtube'
version = 'v3'
youtube = build(service_name, version, developerKey=api_key)


def get_channel_stats(channelName):
    """
    Gets the basic stats for a YouTube channel

    Parameters
    ----------
    channelName : str
        The YouTube channels username
    Returns:
    ----------
    Dictionary
    """
    channel_id = get_channel_id(channelName)   
    request = youtube.channels().list( 
        part='statistics',
        id = channel_id
    )

    response = request.execute()

    return response

def get_channel_id(channelName):
    """
    Scrapes a YouTube channels main-page for their ID

    Parameters
    ----------
    channleName : str
        The YouTube channels username
    Returns:
    ----------
    str:
        The ID
    """

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    user = channelName
    url = f'http://www.youtube.com/c/{user}'

    results = requests.get(url,headers=headers)
    doc = BeautifulSoup(results.text, "html.parser")
    
    tags = doc.find('meta', itemprop="channelId")
    id = tags['content']

    return id



if __name__ == "__main__":

    print(get_channel_stats("CreatedTechOfficial"))
   
   
    
   

   


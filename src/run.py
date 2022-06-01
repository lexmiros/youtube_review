from GetData import *
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

if __name__ == "__main__":
    print(get_channel_stats("CreatedTechOfficial"))
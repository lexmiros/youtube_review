
from src.CleanData import *
from src import CWD
from dotenv import load_dotenv
from src.YouTube import YoutubeStats
import pandas as pd
import json
from datetime import datetime, timedelta
import os




if __name__ == "__main__":
    #channel_name = "CreatedTechOfficial"
    channel_name = "TYLER1LOL"
    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_search = os.getenv("API_SEARCH")
  
    yt = YoutubeStats(api_key, api_search, channel_name)
    yt.get_channel_id()
    yt.get_channel_statistics()
    yt.get_channel_video_data()
    yt.dump()
    
    df = set_date_time(channel_name)
    print(df)








    """

    example = df["Published"]
    example = example[0]
    print(example)
    example = example + timedelta(hours = 10)
    print(example)


    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_search = os.getenv("API_SEARCH")
    channelName = "CreatedTechOfficial"
    channel_id = get_channel_id(channelName)
    yt = YoutubeStats(api_key, api_search, channelName)
    yt.get_channel_id()
    yt.get_channel_statistics()
    yt.get_channel_video_data()
    yt.dump()
    """
   


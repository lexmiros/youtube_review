
from src.CleanData import *
from src import CWD
from dotenv import load_dotenv
from src.YouTube import YoutubeStats
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import re




if __name__ == "__main__":
    channel_name = "TYLER1LOL"

    df = add_cumulative_cols(channel_name)
    print(df)





    """
    #channel_name = "CreatedTechOfficial"
    #channel_name = "TYLER1LOL"
    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_search = os.getenv("API_SEARCH")
    yt = YoutubeStats(api_key, api_search, channel_name)
    yt.get_channel_id()
    yt.get_channel_statistics()
    yt.get_channel_video_data()
    yt.dump()

    """
   


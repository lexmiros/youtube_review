
from src.GetData import *
import os
from dotenv import load_dotenv
from src.YouTube import YoutubeStats
import pandas as pd
from src import CWD



if __name__ == "__main__":
    channelName = "CreatedTechOfficial"
    
    
    #data_loc = f"{CWD}\json\{channelName}.json"
    #df = pd.read_json(data_loc)

    #df = pd.DataFrame(df)
    #print(df)










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
    
   


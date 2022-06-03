
from src.GetData import *
import os
from dotenv import load_dotenv
from src.statistics import YoutubeStats



if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_search = os.getenv("API_SEARCH")
    channelName = "CreatedTechOfficial"
    channel_id = get_channel_id(channelName)
    yt = YoutubeStats(api_key, api_search, channel_id, channelName)
    yt.get_channel_statistics()
    yt.get_channel_video_data()
    yt.dump()

   


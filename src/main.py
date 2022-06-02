
from GetData import *
import os
from dotenv import load_dotenv
from statistics import YoutubeStats


#Building variables
load_dotenv()
api_key = os.getenv("API_KEY")
api_search = os.getenv("API_SEARCH")
channelName = "CreatedTechOfficial"
channel_id = get_channel_id(channelName)




if __name__ == "__main__":
    yt = YoutubeStats(api_key, api_search, channel_id)
    #data = yt.get_channel_statistics()
    #yt.dump()

    data = yt.get_channel_video_data()
    print(data)


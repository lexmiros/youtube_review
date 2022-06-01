
from GetData import *
import os
from dotenv import load_dotenv
from statistics import YoutubeStats


#Building variables
load_dotenv()
api_key = os.getenv("API_KEY")
channelName = "CreatedTechOfficial"
channel_id = get_channel_id(channelName)




if __name__ == "__main__":
    yt = YoutubeStats(api_key, channel_id)
    data = yt.get_channel_statistics()
    yt.dump()
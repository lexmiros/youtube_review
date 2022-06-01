import re
import requests
import json

class YoutubeStats:

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None

    def get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0]["statistics"]
        except:
            data = None
        self.channel_statistics = data

        return data
    
    def dump(self):
        if self.channel_statistics is None:
            return
        channel_title = "TODO" #TODO get channel name from data
        channel_title = channel_title.replace(" ", "_").lower()
        file_name = f"{channel_title}.json"

        with open(file_name, "w") as f:
            json.dump(self.channel_statistics, f, indent=4)
        print('file dumped')



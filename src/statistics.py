import re
import requests
import json

class YoutubeStats:

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None

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
    
    

    def get_channel_video_data(self):
        video = self._get_channel_videos(limit=50)
        print(video)

    def _get_channel_videos_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        videos = dict()

        if "items" not in data:
            return videos, None
            
        item_data = data["items"]
        nextPageToken = data.get("nextPageToken", None)
        
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == "youtube#video":
                    video_id = item['id']['videoId']
                    videos[video_id] = dict()
            except KeyError:
                print("No video IDs found")
        return videos, nextPageToken



    def _get_channel_videos(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search/?key={self.api_key}&channelId={self.channel_id}&part=id&order=date'
        if limit is not None and isinstance(limit, int):
            url += f"&maxResults={str(limit)}"

        vid, npt = self._get_channel_videos_per_page(url)

        i = 0
        while(npt is not None and i < 10):

            nextUrl = url + f"&pageToken={npt}"
            next_vid, npt = self._get_channel_videos_per_page(nextUrl)
            vid.update(next_vid)

            i +=1
        return vid

    def dump(self):
        if self.channel_statistics is None:
            return
        channel_title = "TODO" #TODO get channel name from data
        channel_title = channel_title.replace(" ", "_").lower()
        file_name = f"{channel_title}.json"

        with open(file_name, "w") as f:
            json.dump(self.channel_statistics, f, indent=4)
        print('file dumped')
        

        



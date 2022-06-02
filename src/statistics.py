import re
import requests
import json

class YoutubeStats:

    def __init__(self, api_key, api_search ,channel_id, channel_name):
        self.api_key = api_key
        self.api_search = api_search
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_statistics = None
        self.video_data = None
        self.comments = None

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

        #Get a dictionary with video IDs as the keys
        data = self._get_channel_videos(limit=50)

        #Create empty lists
        video_id_list = []
        video_id_subset = []
    
        #Get each id and add to list
        for id in data:
            video_id_list.append(id)

        #For every 50 IDs, add to a list, convert to a single comma seperated string
        #Request statistics for the 50 Ids, and append to data dictionary based on key
        #Reset the list after 50 ids, or at end of Ids

        #For all ids in the video ID list
        for number, id in enumerate(video_id_list):

            #If its a multiple of 50 or the end
            if (number + 1) % 50 == 0 or (number+1) == len(video_id_list):

                #Append entr to the subset list
                video_id_subset.append(id)
                #Convert from list to a single string
                video_id_string = ','.join(str(e) for e in video_id_subset)
                #Create query URL for video statistics
                url = f"https://www.googleapis.com/youtube/v3/videos?key={self.api_key}&part=statistics&id={video_id_string}"
                #Get query 
                json_url = requests.get(url)
                data_video = json.loads(json_url.text)
                #Get into items list from query results from video statistics
                data_video_items = data_video["items"]

                #For each entry in items list query result from video statistics
                for entry in data_video_items:
                    #Get the video ID, and stats, and add to data dictionary on ID
                    new_id = entry["id"]
                    new_data = entry["statistics"]
                    data[new_id]["statistics"] = new_data
                
                #Reset list
                video_id_subset = []

            else: 
                video_id_subset.append(id)

        self.video_data = data
                       
        return data
        

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
                    videos[video_id] = {"statistics":{}, "snippet":{}}
                    videos[video_id]["snippet"] = item["snippet"]
            except KeyError:
                print("No video IDs found")
        return videos, nextPageToken



    def _get_channel_videos(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search/?key={self.api_search}&channelId={self.channel_id}&part=snippet&order=date'
        
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
        if self.channel_statistics is None or self.video_data is None:
            return
        file_name = f"{self.channel_name}.json"
        x = {
            "channel_stats" : self.channel_statistics,
            "Videos" : self.video_data
        }
        with open(file_name, "w") as f:
            json.dump(x, f, indent=4)
        print('file dumped')
        

        



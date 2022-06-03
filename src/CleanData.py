import pandas as pd
import json
from src import CWD
from datetime import datetime, timedelta


def get_stats(channel_name):
    """
    Gets the total view count for a channel

    Parameters
    ----------
    channel_name : str
        The name of the channel
    Returns
    -------
    int:
        Number of views
    """

    json_filepath = (f"{CWD}\json\{channel_name}.json")
    with open(json_filepath, 'r') as j:
        content = json.loads(j.read())

    view_count = content["channel_stats"]["viewCount"]
    view_count = int(view_count)

    subscriber_count = content["channel_stats"]["subscriberCount"]
    subscriber_count = int(subscriber_count)

    video_count = content["channel_stats"]["videoCount"]
    video_count = int(video_count)

    return view_count, subscriber_count, video_count



def get_video_stats(channel_name):
    """
    """
    json_filepath = (f"{CWD}\json\{channel_name}.json")
    with open(json_filepath, 'r') as j:
        contents = json.loads(j.read())

    video_view_list = []
    video_like_list = []
    video_comment_list = []
    video_duration_list = []
    video_published_list = []
    video_title_list = []
    video_description_list = []


    for key in contents["Videos"]:
        video_view_list.append(contents["Videos"][key]["statistics"]["viewCount"])
        video_like_list.append(contents["Videos"][key]["statistics"]["likeCount"])
        video_comment_list.append(contents["Videos"][key]["statistics"]["commentCount"])
        video_duration_list.append(contents["Videos"][key]["duration"])
        video_published_list.append(contents["Videos"][key]["snippet"]["publishedAt"])
        video_title_list.append(contents["Videos"][key]["snippet"]["title"])
        video_description_list.append(contents["Videos"][key]["snippet"]["description"])

    return (video_view_list, video_like_list, video_comment_list, 
    video_duration_list, video_published_list, video_title_list, video_description_list)

def build_df(channel_name):
    """
    """
    video_data = get_video_stats(channel_name)
  
    df = pd.DataFrame()
    df["Views"] = video_data[0]
    df["Likes"] = video_data[1]
    df["Comments"] = video_data[2]
    df["Duration"] = video_data[3]
    df["Published"] = video_data[4]
    df["Title"] = video_data[5]
    df["Description"] = video_data[6]

    return df

def _build_time_bucket(row):
    
    if (row >= 0) and (row < 6):
        row = "[0-6)"
    elif (row >= 6) and (row < 12):
        row = "[6-12)"
    elif (row >= 12) and (row < 18):
        row = "[12-18)"
    else:
        row = "[18,24)"
    
    return row

def set_date_time(channel_name):
    """
    """
    #Hour offset between UTC and Brisbane UTC+10
    offset = 10
    df = build_df(channel_name)

    #Convert to Brisbane time
    df["Published"] = df["Published"].apply(lambda row: datetime.strptime(row, "%Y-%m-%dT%H:%M:%SZ"))
    df["Published"] = df["Published"].apply(lambda row: row + timedelta(hours = offset))
    df["Year"] = df["Published"].apply(lambda row: row.year)
    df["Month"] = df["Published"].apply(lambda row: row.month)
    df["Hour"] = df["Published"].apply(lambda row: row.hour)
    df["Time Bucket"] = df["Hour"].apply(_build_time_bucket)

    return df
    

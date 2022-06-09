from numpy import add
import pandas as pd
import json
from src import CWD
from datetime import datetime, timedelta
import re


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
        try:
            video_view_list.append(contents["Videos"][key]["statistics"]["viewCount"])
        except:
            video_view_list.append(0)
            
        try:    
            video_like_list.append(contents["Videos"][key]["statistics"]["likeCount"])
        except:
            video_like_list.append(0)
        
        try:
            video_comment_list.append(contents["Videos"][key]["statistics"]["commentCount"])
        except:
            video_comment_list.append(0)
        try:    
            video_duration_list.append(contents["Videos"][key]["duration"])
        except:
            video_duration_list.append(0)
        try:    
            video_published_list.append(contents["Videos"][key]["snippet"]["publishedAt"])
        except:
            video_published_list.append(0)
        try:    
            video_title_list.append(contents["Videos"][key]["snippet"]["title"])
        except:
            video_title_list.append(0)
        try:
            video_description_list.append(contents["Videos"][key]["snippet"]["description"])
        except:
            video_description_list.append(0)
       

    return (video_view_list, video_like_list, video_comment_list, 
    video_duration_list, video_published_list, video_title_list, video_description_list)

def build_df(channel_name):
    """
    """
    video_data = get_video_stats(channel_name)
  
    df = pd.DataFrame()
    df["Views"] = video_data[0]
    df["Views"] = df["Views"].astype(int)
    df["Likes"] = video_data[1]
    df["Likes"] = df["Likes"].astype(int)
    df["Comments"] = video_data[2]
    df["Comments"] = df["Comments"].astype(int)
    df["Duration"] = video_data[3]
    df["Published"] = video_data[4]
    df["Title"] = video_data[5]
    df["Description"] = video_data[6]
    
    df = df[ (df["Views"] != 0) | (df["Likes"] != 0) | df["Comments"] != 0]

    return df

def _build_time_bucket(row):
    
    if (row >= 0) and (row < 3):
        row = "0-3"
    elif (row >= 3) and (row < 6):
        row = "3-6"
    elif (row >= 6) and (row < 9):
        row = "6-9"
    elif (row >= 9) and (row < 12):
        row = "9-12"
    elif (row >= 12) and (row < 15):
        row = "12-15"
    elif (row >= 15) and (row < 18):
        row = "15-18"
    elif (row >= 18) and (row < 21):
        row = "18-21"
    else:
        row = "21-24"
    
    return row

def _duration_convert(row):
    try:
        mins = re.findall("(\d*)(?=M)", row)
        mins = mins[0]
    except:
        mins = 0
    try:
        secs = re.findall("(\d*)(?=S)", row)
        secs = secs[0]
    except:
        secs = 0


    time = int(mins) + (int(secs)/60)

    return time

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
    df["Day"] = df["Published"].apply(lambda row: row.day)
    df["Hour"] = df["Published"].apply(lambda row: row.hour)
    df["Time Bucket"] = df["Hour"].apply(_build_time_bucket)
    df["Duration"] = df["Duration"].apply(_duration_convert)
    

    return df


def impute_cols(channel_name):

    df = set_date_time(channel_name)
    df["cum Views"] = df["Views"].cumsum()
    df["cum Likes"] = df["Likes"].cumsum()
    df["cum Comments"] = df["Comments"].cumsum()
    df["Title length"] = df["Title"].apply(lambda row: len(row))
    df["Title length"] = df["Title length"].astype(int)
    df["Like Ratio"] = df.apply(lambda row: row["Likes"] / row["Views"], axis=1)
    df["Comment Ratio"] = df.apply(lambda row: row["Comments"] / row["Views"], axis=1)

    return df



def build_df_clean(channel_name):

    df = impute_cols(channel_name)

    return df





    


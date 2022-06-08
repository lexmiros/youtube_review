from cmath import nan
import pandas as pd
from datetime import datetime, timedelta
import math


def get_avg_post_hours(df):

    hours_in_day = 24
    
    time_sorted_df = df.sort_values(by="Published")
    day_alpha = time_sorted_df["Published"][len(time_sorted_df)-1]
    day_omega = time_sorted_df["Published"][0]

    total_days = (day_omega - day_alpha).days
    total_hours = total_days * hours_in_day
    total_videos = len(df)

    posts_per_days = total_hours / total_videos
    posts_per_days = round(posts_per_days)

    return posts_per_days


def get_post_timeline(df):
    
    total_years = df["Year"].sort_values().unique()
    
    total_months = []

    for i in range(1,13):
        total_months.append(i)

    labels = []
    total_posts = []

    #Builds a list of year-date months and the count of posts during them
    for year in total_years:
        for month in total_months:
            labels.append(f"{year}-{month}")

            x = df[(df["Year"] == year) & (df["Month"] == month)]
            x = len(x)

            total_posts.append(x)
    #combine labels, posts for combined iteration        
    z = zip(labels, total_posts)
    
    #Reset values now saved in z
    labels = []
    total_posts = []
    
    #Remove dates with 0 posts
    for values in z:
        if values[1] != 0:
            labels.append(values[0])
            total_posts.append(values[1])

    return (labels, total_posts)

def get_views_timeline(df):
    """"""
    
    total_years = df["Year"].sort_values().unique()
    
    total_months = []

    for i in range(1,13):
        total_months.append(i)

    labels = []
    total_views = []

    #Builds a list of year-date months and the count of posts during them
    for year in total_years:
        for month in total_months:
            labels.append(f"{year}-{month}")

            df_month = df[(df["Year"] == year) & (df["Month"] == month)]
            avg_views = df_month["Views"].mean()
            
            if math.isnan(avg_views):
                avg_views = 0
                
            avg_views = round(avg_views)

            total_views.append(avg_views)

    #combine labels, posts for combined iteration        
    z = zip(labels, total_views)
    
    #Reset values now saved in z
    labels = []
    total_views = []
    
    #Remove dates with 0 posts
    for values in z:
        if values[1] != 0:
            labels.append(values[0])
            total_views.append(values[1])

    return (labels, total_views)

def get_views_post_time(df):
    
    labels = ["0-3", "3-6", "6-9", "9-12", "12-15", "15-18", "18-21", "21-0"]
    time_views = []
    
    for time in labels:
        df_t = df[df["Time Bucket"] == time]
        avg_views = df_t["Views"].mean()
        if math.isnan(avg_views):
                avg_views = 0
        avg_views = round(avg_views)
        
        time_views.append(avg_views)
        
    return (labels, time_views)

def get_views_title_len(df):
    
    max_num = max(df["Title length"])
    bin_incremenet = math.ceil(max_num / 7) 
    
    j = 0
    labels = []
    values = []
    for i in range(bin_incremenet, max_num, bin_incremenet):
        label = f"Bin {j} - {i}"
        labels.append(label)
        
        df_i = df[(df["Title length"] >= j) & (df["Title length"] < i)]
        value = df_i["Views"].mean()
        if math.isnan(value):
            value = 0
            
        value = round(value)
        values.append(value)
        
        j = j + bin_incremenet
        
    return (labels, values)

def get_views_duration(df):
    
    max_num = max(df["Duration"])
    max_num = math.ceil(max_num)
    bin_incremenet = math.ceil(max_num / 7) 
    
    
    j = 0
    labels = []
    values = []
    for i in range(bin_incremenet, max_num, bin_incremenet):
        
        label = f"Bin {j} - {i}"
        labels.append(label)
        
        df_i = df[(df["Duration"] >= j) & (df["Duration"] < i)]
        value = df_i["Views"].mean()
        if math.isnan(value):
            value = 0
            
        value = round(value)
        values.append(value)
        j = j + bin_incremenet
        
    return (labels, values)
import pandas as pd
from datetime import datetime, timedelta


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

    x = df[(df["Year"] == 2022) & (df["Month"] == 6)]
    x = len(x)

    labels = []
    total_posts = []

    #Builds a list of year-date months and the count of posts during them
    for year in total_years:
        for month in total_months:
            labels.append(f"{year}-{month}")

            x = df[(df["Year"] == year) & (df["Month"] == month)]
            x = len(x)

            total_posts.append(x)

    #Removes trailing zeros due to dates not yet occured
    for i in range(len(total_posts) -1 ,0,-1):
        if total_posts[i] == 0:
            total_posts.pop(i)
        else:
            break
    
    #Trims labels to match posts
    labels = labels[0:len(total_posts)]

    return (labels, total_posts)


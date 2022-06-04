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





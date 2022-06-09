from cmath import nan
import pandas as pd
from datetime import datetime, timedelta
import math
import spacy
from collections import Counter

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

def get_mean_views_timeline(df):
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

def get_views_timeline(df):
    
    df = df.sort_values("Published")
    data = df["Views"].to_list()
    date_list = []
    days = df["Day"].to_list()
    months = df["Month"].to_list()
    years = df["Year"].to_list()
    
    z = zip(days, months, years)
    
    for value in z:
        date = f"{value[2]}-{value[1]}"
        date_list.append(date)
        
    
    
        
    return (date_list, data)


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
    bin_incremenet = math.ceil(max_num / 10) 
    
    j = 0
    labels = []
    values = []
    for i in range(bin_incremenet, max_num, bin_incremenet):
        label = f"{j} - {i}"
        labels.append(label)
        
        df_i = df[(df["Title length"] >= j) & (df["Title length"] < i)]
        value = df_i["Views"].mean()
        if math.isnan(value):
            value = 0
            
        value = round(value)
        values.append(value)
        
        j = j + bin_incremenet
        
    z = zip(labels, values)
    
    
    labels = []
    values = []
    
    #Remove dates with 0 posts
    for value in z:
        if value[1] != 0:
            labels.append(value[0])
            values.append(value[1])
        
    return (labels, values)

def get_views_duration(df):
    
    max_num = max(df["Duration"])
    max_num = math.ceil(max_num)
    bin_incremenet = math.ceil(max_num / 10) 
    
    
    j = 0
    labels = []
    values = []
    for i in range(bin_incremenet, max_num, bin_incremenet):
        
        label = f"{j} - {i}"
        labels.append(label)
        
        df_i = df[(df["Duration"] >= j) & (df["Duration"] < i)]
        value = df_i["Views"].mean()
        if math.isnan(value):
            value = 0
            
        value = round(value)
        values.append(value)
        j = j + bin_incremenet
    
    z = zip(labels, values)
    
    
    labels = []
    values = []
    
    #Remove dates with 0 posts
    for value in z:
        if value[1] != 0:
            labels.append(value[0])
            values.append(value[1])
        
    return (labels, values)

def corr_duration(df):
    """"""
    dur_corr = df["Views"].corr(df["Duration"])
    dur_corr = round(dur_corr, 4)
    dur_rating = _corr_rating(dur_corr)
    
    return (dur_corr, dur_rating)
    
    

def corr_title(df):
    title_corr = df["Views"].corr(df["Title length"])
    title_corr = round(title_corr, 4)
    title_rating = _corr_rating(title_corr)
    
    return (title_corr, title_rating)

    
def _corr_rating(corr):
    if corr >= 0:
        suffix = "positive correlation"
    else:
        suffix = "negative correlation"
    corr = abs(corr)
    if corr <= 0.19:
        rating = "Very low"
    elif corr < 0.2 and corr <= 0.39:
        rating = "Low"
    elif corr < 0.4 and corr <= 0.59:
        rating = "Moderate"
    elif corr < 0.6 and corr <= 0.79:
        rating = "High"
    elif corr < 0.8 and corr <= 1:
        rating = "Very high"
    
    return f"{rating} {suffix}"
   
    
    

def get_like_ratio_date(df):
    
    data = df["Like Ratio"].to_list()
    date_list = []
    days = df["Day"].to_list()
    months = df["Month"].to_list()
    years = df["Year"].to_list()
    
    z = zip(days, months, years)
    
    for value in z:
        date = f"{value[2]}-{value[1]}"
        date_list.append(date)
        
   
        
    return (date_list, data)


def get_comment_ratio_date(df):
    
    data = df["Comment Ratio"].to_list()
    date_list = []
    days = df["Day"].to_list()
    months = df["Month"].to_list()
    years = df["Year"].to_list()
    
    z = zip(days, months, years)
    
    for value in z:
        date = f"{value[2]}-{value[1]}"
        date_list.append(date)
        
   
        
    return (date_list, data)
  
    
def get_title_count(df):
    x = df["Title"].to_list()
    words_str = ""
    for words in x:
        words_str = words_str + words
    
    #Remove word formatting
    words_formatting = [",", "...", "(", ")", ":", "-", ".", "+", "=", "&", "?", "!", "#39;S"]
    for format in words_formatting:
        words_str = words_str.replace(format, ' ')

    en = spacy.load('en_core_web_sm')
    sw_spacy = en.Defaults.stop_words
    
    words = [word for word in words_str.split() if word.lower() not in sw_spacy]
    new_text = " ".join(words)

    words = new_text.split()
    wordCount = Counter(words)
    
    return wordCount
    
def get_description_count(df):
    
    x = df['Description'].to_list()
    words_str = ""
    for words in x:
        words_str = words_str + words
        
    #Remove word formatting
    words_formatting = [",", "...", "(", ")", ":", "-", ".", "+", "=", "&", "?", "!", "#39;S"]
    for format in words_formatting:
        words_str = words_str.replace(format, ' ')
    en = spacy.load('en_core_web_sm')
    sw_spacy = en.Defaults.stop_words
    
    words = [word for word in words_str.split() if word.lower() not in sw_spacy]
    new_text = " ".join(words)
    

    words = new_text.split()
    wordCount = Counter(words)
    
    return wordCount


def get_top_desc_values(df):
    
    dict = get_description_count(df)
    dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
    
    
    words = []
    counts = []
    for word in dict:
        words.append(word)
        counts.append(dict[word])
        
    top_words = []
    top_counts = []
    
    for i in range(len(words), (len(words)-21), -1):
        try:
            top_words.append(words[i])
            top_counts.append(counts[i])   
        except:
            pass
    
    return (top_words, top_counts)

def get_top_title_values(df):
    
    dict = get_title_count(df)
    dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
    
    
    words = []
    counts = []
    for word in dict:
        words.append(word)
        counts.append(dict[word])
        
    top_words = []
    top_counts = []
    
    for i in range(len(words), (len(words)-21), -1):
        try:
            top_words.append(words[i])
            top_counts.append(counts[i])   
        except:
            pass
    
    return (top_words, top_counts)
    
    

 
    
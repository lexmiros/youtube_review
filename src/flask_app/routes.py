from src.CleanData import build_df_clean, get_stats
from src.analysis import get_avg_post_hours
from src.flask_app import app
from flask import redirect, render_template, url_for
from src.flask_app.forms import LandingForm
from dotenv import load_dotenv
from src.YouTube import YoutubeStats
import os

@app.route("/",  methods = ["POST", "GET"])
def landing():
    """
    """
    form = LandingForm()
    test = "False"

    if form.validate_on_submit():

        user = form.user.data
        user = user.upper()

        if user == "":
            user = "TYLER1LOL"
            test = "True"

        return redirect(url_for("loading", user = user, test = test))


    return render_template("landing.html", form = form)

@app.route("/loading/<user>/<test>")
def loading(user, test):
    """"""
    if test == "False":
        channel_name = user
        load_dotenv()
        api_key = os.getenv("API_KEY")
        api_search = os.getenv("API_SEARCH")
        yt = YoutubeStats(api_key, api_search, channel_name)
        yt.get_channel_id()
        yt.get_channel_statistics()
        yt.get_channel_video_data()
        yt.dump()

    return redirect(url_for("overview", user = user, test = test))



@app.route("/overview/<user>/<test>", methods = ["POST", "GET"])
def overview(user, test):

    #Get data
    df = build_df_clean(user)
    view_count, subscriber_count, video_count = get_stats(user)
    
    #Overview numbers
    total_found = len(df)
    view_count = (format(view_count, ',d'))
    subscriber_count = (format(subscriber_count, ',d'))
    video_count = (format(video_count, ',d'))

    #Averages
    avg_likes = round(df["Likes"].mean())
    avg_likes = (format(avg_likes, ',d'))

    avg_comments = round(df["Comments"].mean())
    avg_comments = (format(avg_comments, ',d'))

    avg_views = round(df["Views"].mean())
    avg_views = (format(avg_views, ',d'))

    avg_duration = round(df["Duration"].mean())
    avg_duration = (format(avg_duration, ',d'))
    
    average_post = get_avg_post_hours(df)


    
    
    return render_template("overview.html", 
    user = user, total_found = total_found, view_count = view_count, subscriber_count = subscriber_count, video_count = video_count,
    avg_likes = avg_likes, avg_comments = avg_comments, avg_views = avg_views, avg_duration = avg_duration, average_post = average_post
    )

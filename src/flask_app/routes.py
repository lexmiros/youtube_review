from src.CleanData import build_df, build_df_clean
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

    df = build_df_clean(user)

    total = len(df)

    
    
    return render_template("overview.html", user = user, total = total)

from asyncio import get_running_loop
from src.flask_app import app
from flask import render_template, url_for
from src.flask_app.forms import LandingForm

@app.route("/")
def landing():
    """
    """
    form = LandingForm()

    return render_template("landing.html", form = form)
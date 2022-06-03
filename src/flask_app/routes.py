from asyncio import get_running_loop
from src.flask_app import app
from flask import render_template, url_for

@app.route("/")
def landing():
    """
    """
    return render_template("landing.html")
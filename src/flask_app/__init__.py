from flask import Flask
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()
secret_key = os.getenv("FLASK_KEY")
app.config["SECRET_KEY"] = secret_key
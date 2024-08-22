from pymongo import MongoClient
from dotenv import dotenv_values
import os

# get the dotenv path
ENV_VALUE = dotenv_values("./env/credentials.env")

CONNECTION_STRING = ENV_VALUE["CONNECTION_STRING"]
HOST_ID = ENV_VALUE["HOST_ID"]
PORT_ID = ENV_VALUE["PORT_ID"]
RELOAD_STATE = ENV_VALUE["RELOAD_STATE"]
DEBUG = ENV_VALUE.get("DEBUG", "False") # provide default value is not set
SECRET_KEY = ENV_VALUE["SECRET_KEY"]
ALGORITHM = ENV_VALUE["ALGORITHM"]
GEMINI_KEY = ENV_VALUE["GEMINI_KEY"]

UNSPLASH_ACCESS_KEY_1 = ENV_VALUE["UNSPLASH_ACCESS_KEY1"]
UNSPLASH_ACCESS_KEY_2 = ENV_VALUE["UNSPLASH_ACCESS_KEY2"]

GOOGLE_CLIENT_ID = ENV_VALUE["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = ENV_VALUE["GOOGLE_CLIENT_SECRET"]
GOOGLE_REDIRECT_URI = ENV_VALUE["GOOGLE_REDIRECT_URI"]

# get connection
def connect_to_database():
    client = MongoClient(CONNECTION_STRING)
    return client
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

# using os
MONGO_RUI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# get connection
def connect_to_database():
    client = MongoClient(MONGO_RUI)
    return client
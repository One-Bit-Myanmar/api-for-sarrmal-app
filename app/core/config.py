from pymongo import MongoClient
from dotenv import dotenv_values

# get the dotenv path
ENV_VALUE = dotenv_values("./env/credentials.env")

CONNECTION_STRING = ENV_VALUE["CONNECTION_STRING"]
HOST_ID = ENV_VALUE["HOST_ID"]
PORT_ID = ENV_VALUE["PORT_ID"]
RELOAD_STATE = ENV_VALUE["RELOAD_STATE"]

DEBUG = ENV_VALUE.get("DEBUG", "False") # provide default value is not set

# get connection
def connect_to_database():
    client = MongoClient(CONNECTION_STRING)
    return client # return mongoDB client
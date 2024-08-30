from pymongo import MongoClient
import os


# Access environment variables
CONNECTION_STRING = os.environ["CONNECTION_STRING"]
HOST_ID = os.environ["HOST_ID"]  # Default to 0.0.0.0 if not set
PORT_ID = int(os.environ["PORT_ID"])  # Default to 8000 and ensure it's an integer
RELOAD_STATE = os.environ["RELOAD_STATE"].lower() == "true"  # Convert to boolean
DEBUG = os.environ["DEBUG"].lower() == "true"  # Convert to boolean
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
GEMINI_KEY = os.environ["GEMINI_KEY"]
UNSPLASH_ACCESS_KEY_1 = os.environ["UNSPLASH_ACCESS_KEY1"]
UNSPLASH_ACCESS_KEY_2 = os.environ["UNSPLASH_ACCESS_KEY2"]
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
GOOGLE_REDIRECT_URI = os.environ["GOOGLE_REDIRECT_URI"]
INITIAL_TOKEN = os.environ["TOKEN_VALUE"]
REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
OAUTH_CLIENT_ID = os.environ["OAUTH_CLIENT_ID"]
OAUTH_CLIENT_SECRET = os.environ["OAUTH_CLIENT_SECRET"]
OAUTH_API = os.environ["OAUTH_API"]
SEARCH_ENGINE_ID = os.environ["SEARCH_ENGINE_ID"]

# Google Image Search API
OAUTH_API_1=os.environ("OAUTH_API_1")
OAUTH_API_2=os.environ("OAUTH_API_2")
OAUTH_API_3=os.environ("OAUTH_API_3")
OAUTH_API_4=os.environ("OAUTH_API_4")
OAUTH_API_5=os.environ("OAUTH_API_5")
OAUTH_API_6=os.environ("OAUTH_API_6")

# get connection
def connect_to_database():
    client = MongoClient(CONNECTION_STRING)
    return client
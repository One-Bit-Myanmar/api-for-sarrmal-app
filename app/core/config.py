from pymongo import MongoClient
import os


# Access environment variables
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
HOST_ID = os.getenv("HOST_ID", "0.0.0.0")  # Default to 0.0.0.0 if not set
PORT_ID = int(os.getenv("PORT_ID", 8000))  # Default to 8000 and ensure it's an integer
RELOAD_STATE = os.getenv("RELOAD_STATE", "False").lower() == "true"  # Convert to boolean
DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # Convert to boolean
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
GEMINI_KEY = os.getenv("GEMINI_KEY")
UNSPLASH_ACCESS_KEY_1 = os.getenv("UNSPLASH_ACCESS_KEY_1")
UNSPLASH_ACCESS_KEY_2 = os.getenv("UNSPLASH_ACCESS_KEY_2")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# get connection
def connect_to_database():
    client = MongoClient(CONNECTION_STRING)
    return client
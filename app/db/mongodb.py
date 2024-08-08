
from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values("credentials.env")

def connectToDatabase():
    db = MongoClient(config["MONGO_CONNECTION_STRING"])
    print(db)
    return db

from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values("credentials.env")

def connectToDatabase():
    db = MongoClient("mongodb+srv://zedzedekiah05:hXFcDy6qLzuOIFi2@cluster0.c9h2w3p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    print(db)
    return db

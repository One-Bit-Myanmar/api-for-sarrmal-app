from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import MongoClient
from dotenv import dotenv_values
from routes import router

config = dotenv_values("credentials.env")

async def connectToDatabase():
    db = MongoClient(config["MONGO_CONNECTION_STRING"])
    print(db)
    return db

@asynccontextmanager
async def lifespan(app: FastAPI):
    dbHost = await connectToDatabase()
    app.players = dbHost.tournament.players
    print("startup has begun!!")
    yield
    print("shutdown has begun!!")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
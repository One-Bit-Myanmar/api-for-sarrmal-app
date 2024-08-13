from fastapi import FastAPI, HTTPException, Depends, Request
from contextlib import asynccontextmanager
import uvicorn

# get configured env values
from app.core.config import HOST_ID, PORT_ID, RELOAD_STATE


app = FastAPI()

# for cors middleware /// aka default middleware

# include the middleware here

# for routes from app.api.endpoints /// include the routes here


# calling root directory
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to food recommendation app"}

# main method to run the application ///// run api with command
if __name__ == "__main__":
    uvicorn.run(app, host=HOST_ID, port=PORT_ID, reload=RELOAD_STATE)




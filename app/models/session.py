from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from app.db.mongodb import connectToDatabase

# additional feature
from apscheduler.schedulers.background import BackgroundScheduler
# function to delete expired sessions
def delete_expired_sessions():
    db = connectToDatabase()
    expiry_time = datetime.utcnow() - timedelta(weeks=1)
    sessions_collection = db["Cluster0"]["sessions"]
    sessions_collection.delete_many({"updated_at": {"$lt": expiry_time}})

# Scheduler to run the cleanup task every day
scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_sessions, 'interval', days=1)
scheduler.start()


class Session(BaseModel):
    email: EmailStr
    access_token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()

    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
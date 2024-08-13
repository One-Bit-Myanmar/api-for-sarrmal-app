from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timedelta

class Session(BaseModel):
    user_id: str
    access_token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()

    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
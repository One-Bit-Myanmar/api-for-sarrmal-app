from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Chat(BaseModel):
    chat_id: int
    user_id: str
    date: datetime = Field(default_factory=datetime.utcnow)
    message: str
    response: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()
    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
            
# user request model to make an api request to open ai chat bot
class RequestModel(BaseModel):
    user_id: str
    message: str

# for the user message editing
class ChatUpdateModel(BaseModel):
    user_id: str
    message: str
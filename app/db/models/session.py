from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Action(BaseModel):
    action_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Session(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    session_start: datetime = Field(default_factory=datetime.utcnow)
    session_end: Optional[datetime]
    ip_address: Optional[str]
    device: Optional[str]
    actions: List[Action] = []

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

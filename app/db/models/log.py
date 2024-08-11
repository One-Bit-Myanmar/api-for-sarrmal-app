from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Log(BaseModel):
    error_id: str
    timestamp: str
    level: str
    message: str
    stack_trace: str
    module: str
    ip_address: str
    device: str
    user_id: str
    url: str
    method: str
    tags: list[str]
    resolved: bool
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()
    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()

class RequestInfo(BaseModel):
    url: str
    method: str

class ErrorLog(BaseModel):
    error_id: str
    timestamp: datetime
    level: str
    message: str
    stack_trace: str
    module: str
    ip_address: str
    device: str
    user_id: str
    request: RequestInfo
    tags: list[str]
    resolved: bool
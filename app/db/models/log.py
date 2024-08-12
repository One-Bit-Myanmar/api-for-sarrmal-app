from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re

class Log(BaseModel):
    error_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: str
    message: str
    stack_trace: Optional[str] = None
    module: str
    ip_address: Optional[str] = None
    device: str
    user_id: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
    tags: List[str] = []
    resolved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('ip_address')
    def validate_ip_address(cls, v):
        if v is None:
            return v
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if not re.match(ip_pattern, v):
            raise ValueError('Invalid IP address format')
        return v

    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()

class RequestInfo(BaseModel):
    url: str
    method: str

class ErrorLog(BaseModel):
    error_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: str
    message: str
    stack_trace: Optional[str] = None
    module: str
    ip_address: Optional[str] = None
    device: str
    user_id: Optional[str] = None
    request: RequestInfo
    tags: List[str] = []
    resolved: bool = False

    @validator('ip_address')
    def validate_ip_address(cls, v):
        if v is None:
            return v
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if not re.match(ip_pattern, v):
            raise ValueError('Invalid IP address format')
        return v

    def save(self, update: bool = False):
        pass

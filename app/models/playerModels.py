from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Player(BaseModel):
    id: Optional[str] = Field(default_factory=str, alias="_id")
    name: str
    age: int = Field(gt=0)
    role: str
    team: str
    additional_details: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("role")
    def validate_role(cls, v):
        valid_roles = ["forward", "midfielder", "defender", "goalkeeper"]
        if v.lower() not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        return v
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()

    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
        # Perform save operation to the database
        # For example: db.insert_one(self.dict(by_alias=True))

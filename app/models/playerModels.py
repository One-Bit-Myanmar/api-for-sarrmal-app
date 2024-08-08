from pydantic import BaseModel, Field
from typing import Optional

class Player(BaseModel):
    id: Optional[str] = Field(default_factory=str, alias="_id")
    name: str
    age: int = Field(gt=0)
    role: str
    team: str
    additional_details: str | None = None

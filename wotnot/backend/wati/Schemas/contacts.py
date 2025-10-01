from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Pydantic model
class ContactCreate(BaseModel):
    name: str
    email: Optional[str]
    phone: str
    tags: list[str] = []

class ContactRead(ContactCreate):
    id: int
    created_at: datetime
    
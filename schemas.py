from pydantic import BaseModel, EmailStr
from typing import List
class TemplateCreate(BaseModel):
    name: str
    query: str

class TemplateRead(BaseModel):
    id: int
    name: str
    query: str

    class Config:
        orm_mode = True

class ScheduleQuery(BaseModel):
    name: str
    query: str
    hour: int
    minute: int
    recipients: List[EmailStr]  # Validación estricta de correos electrónicos
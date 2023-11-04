from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from models.dal import DAL
from models.auth import Auth

class Notifications(DAL, BaseModel):
    """Representing table auth"""
    __tablename__ = 'notifications'

    id: Optional[int]
    title: str = ''
    message: str = ''
    ack: Optional[int] = 0
    role: Optional[str] = 'user'
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    target_user_id: int

    @validator('ack')
    @classmethod
    def ack_valid(cls, value):
        if value != 0 and value != 1:
            raise ValueError("Ack must be 1 for true or 0 for false")
        return value

    @validator('role')
    @classmethod
    def role_valid(cls, value):
        if value not in Auth.get_roles():
            raise ValueError("Active must be 1 for true or 0 for false")
        return value

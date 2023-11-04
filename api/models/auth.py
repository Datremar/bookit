from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from models.dal import DAL

class Auth(DAL, BaseModel):
    """Representing table auth"""
    __tablename__ = 'auth'

    id: Optional[int]
    username: str = ''
    password: str = ''
    active: Optional[int] = 1
    role: Optional[str] = 'user'
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

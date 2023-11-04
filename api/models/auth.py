import string
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
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

    @validator('username')
    @classmethod
    def username_valid(cls, value):
        if any(p in value for p in string.punctuation):
            raise ValueError("Username must not include pointuation")
        return value
    
    @validator('active')
    @classmethod
    def active_valid(cls, value):
        if value != 0 and value != 1:
            raise ValueError("Active must be 1 for true or 0 for false")
        return value
        

    @validator('role')
    @classmethod
    def role_valid(cls, value):
        if value not in cls.get_roles():
            raise ValueError("Active must be 1 for true or 0 for false")
        return value

    @classmethod
    def get_roles(cls):
        return ['user', 'admin']

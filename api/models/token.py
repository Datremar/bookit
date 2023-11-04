from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.dal import DAL
import config

class Token(DAL, BaseModel):
    """Representing table token"""
    __tablename__ = 'token'

    id: Optional[int]
    user_id: int = 0
    token: str = config.generate_token()
    expire_date: Optional[datetime] = config.generate_date_delta()

    _token_delta = 12

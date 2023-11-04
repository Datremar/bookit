import dataclasses
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from models.dal import DAL

@dataclasses.dataclass
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

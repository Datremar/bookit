import json
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from models.dal import DAL

class Timesheets(DAL, BaseModel):
    """Representing table auth"""
    __tablename__ = 'notifications'

    id: Optional[int]
    name: str = ''
    timesheet: str = ''
    type: Optional[str] = 'busy'
    active: Optional[int] = 0
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    @validator('timesheet')
    @classmethod
    def timesheet_valid(cls, value):
        try:
            json.loads(value)
        except ValueError as exc:
            raise ValueError("Timesheet must be a valid json") from exc
        return value

    @validator('type')
    @classmethod
    def type_valid(cls, value):
        types = cls.get_types()
        if value not in types:
            raise ValueError("Active must be one of this: " + str(types))
        return value

    @validator('active')
    @classmethod
    def active_valid(cls, value):
        if value not in (0,1):
            raise ValueError("Active must be 1 for true or 0 for false")
        return value

    @classmethod
    def get_types(cls):
        return ['busy', 'free']

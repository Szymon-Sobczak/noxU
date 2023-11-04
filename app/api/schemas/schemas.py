from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """Class representing a user entry base"""
    user_name: str
    user_email: str
    password: str
    is_admin: bool
    is_active: bool


class UserCreate(UserBase):
    """Class representing a user for creating new entry"""


class User(UserBase):
    """Class representing a user for reading existing entry"""
    user_id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """Class representing user for updating existing entry"""
    username: Optional[str] = None
    user_email: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None

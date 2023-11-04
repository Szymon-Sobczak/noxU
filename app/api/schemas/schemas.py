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
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None


class StatusBase(BaseModel):
    """Class representing a status entry base"""
    description: str


class StatusCreate(StatusBase):
    """Class representing a status for creating new entry"""


class Status(StatusBase):
    """Class representing a status for reading existing entry"""
    status_id: int

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    """Class representing an item entry base"""
    item_name: str
    label_number: int


class ItemCreate(ItemBase):
    """Class representing an item for creating new entry"""


class Item(ItemBase):
    """Class representing an item for reading existing entry"""
    item_id: int

    class Config:
        orm_mode = True

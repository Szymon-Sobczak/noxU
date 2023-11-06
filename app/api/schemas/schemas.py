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


class OrderBase(BaseModel):
    """Class representing an Order entry base"""
    order_name: str
    creation_date: datetime


class OrderCreate(OrderBase):
    """Class representing an Order for creating new entry"""


class Order(OrderBase):
    """Class representing an Order for reading existing entry"""
    order_id: int

    class Config:
        orm_mode = True


class OrderUpdate(BaseModel):
    """Class representing Order for updating existing entry"""
    order_name: Optional[str] = None


class OrderContentBase(BaseModel):
    """Class representing an OrderContent entry base"""
    order_id: int
    item_id: int
    quantity: int


class OrderContentCreate(OrderContentBase):
    """Class representing an OrderContent for creating new entry"""


class OrderContent(OrderContentBase):
    """Class representing an OrderContent for reading existing entry"""
    order_item_id: int

    class Config:
        orm_mode = True


class OrderContentUpdate(BaseModel):
    """Class representing OrderContent for updating existing entry"""
    order_id: Optional[int] = None
    item_id: Optional[int] = None
    quantity: Optional[int] = None


class ProductionLogBase(BaseModel):
    """Class representing an ProductionLog entry base"""
    user_id: int
    order_id: int
    status_id: int
    creation_date: datetime
    additional_info: Optional[str] = None


class ProductionLogCreate(ProductionLogBase):
    """Class representing an ProductionLog for creating new entry"""


class ProductionLog(ProductionLogBase):
    """Class representing an ProductionLog for reading existing entry"""
    log_id: int

    class Config:
        orm_mode = True


class ProductionLogUpdate(BaseModel):
    """Class representing ProductionLog for updating existing entry"""
    additional_info: Optional[str] = None

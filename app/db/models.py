"""Database entities models"""
import enum
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """Table storing data on users registered in the system."""

    __tablename__ = "users"

    user_id = Column("user_id", Integer, primary_key=True, index=True)
    user_name = Column("user_name", Integer, nullable=False, unique=True)
    user_email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    is_admin = Column("is_admin", Boolean, nullable=False)
    is_active = Column("is_active", Boolean, nullable=False)

    production_log = relationship("ProductionLog", back_populates="users")


class BasicStatuses(enum.Enum):
    """Contains the basic statuses that must be included 
    in order for the program to work correctly."""
    OK = "ok"
    NOK = "nok"
    NO_QR = "no_qr_code"
    WRONG_QR = "wrong_qr_code"


class ProductionLog(Base):
    """Table storing data about the production process
    - the statuses of individual checks of elements in orders."""

    __tablename__ = "production_log"

    log_id = Column("log_id", Integer, primary_key=True, index=True)
    user_id = Column("user_id", Integer, ForeignKey(
        "users.user_id"), nullable=False)
    order_id = Column("order_id", Integer, ForeignKey(
        "orders.order_id"))
    status = Column("status", Enum(BasicStatuses), nullable=False)
    creation_date = Column("creation_date", DateTime, nullable=False)
    additional_info = Column("additional_info", String)

    users = relationship("User", back_populates="production_log")
    orders = relationship("Order", back_populates="production_log")


class Order(Base):
    """Table storing data with names defined in the order system."""

    __tablename__ = "orders"

    order_id = Column("order_id", Integer, primary_key=True, index=True)
    order_name = Column("order_name", String, nullable=False, unique=True)
    creation_date = Column("creation_date", DateTime)

    production_log = relationship("ProductionLog", back_populates="orders")

    order_content = relationship("OrderContent",
                                 back_populates="order",
                                 cascade='all, delete-orphan',
                                 lazy='joined')


class OrderContent(Base):
    """Table storing data on items included in defined orders."""

    __tablename__ = "order_content"

    order_item_id = Column("order_content_id", Integer,
                           primary_key=True, index=True)
    order_id = Column("order_id", Integer, ForeignKey(
        "orders.order_id"), nullable=False)
    item_id = Column("item_id", Integer, ForeignKey(
        "items.item_id"), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)

    order = relationship("Order", back_populates="order_content")
    items = relationship("Item", back_populates="order_content")


class Item(Base):
    """A table storing data on order elements available
    and recognized by the artificial intelligence model."""

    __tablename__ = "items"

    item_id = Column("item_id", Integer, primary_key=True, index=True)
    item_name = Column("item_name", String, nullable=False, unique=True)
    label_number = Column("label_number", Integer, nullable=False, unique=True)

    order_content = relationship("OrderContent", back_populates="items")

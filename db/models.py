"""Database entities models"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """ """
    __tablename__ = "Users"

    user_id = Column("user_id", Integer, primary_key=True, index=True)
    user_name = Column("user_name", Integer)
    user_email = Column("email", String)
    password = Column("password", String)
    acess_level = Column("access_level", String)


class AccessLevel(Base):
    """ """
    __tablename__ = "access_levels"

    access_level_id = Column()
    description = Column()


class OrderLog(Base):
    """ """
    __tablename__ = "order_log"

    log_entry_id = Column()
    user_id = Column()
    order_id = Column()
    status_id = Column()
    date = Column()
    additional_info = Column()


class Order(Base):
    """ """
    __tablename__ = "orders"

    order__id = Column("order_id", Integer,
                       primary_key=True, index=True)
    order_name = Column("order_name", String)
    creation_date = Column("creation_date", DateTime)


class OderItem(Base):
    """ """
    __tablename__ = "order_items"

    order_item_id = Column("order_item_id", Integer,
                           primary_key=True, index=True)
    order_id = Column("order_id", Integer)
    item_id = Column("item_id", Integer)
    quantity = Column("quantity", Integer)


class Item(Base):
    """ """
    __tablename__ = "items"

    user_id = Column("item_id", Integer, primary_key=True, index=True)
    user_name = Column("name", String)


class Status(Base):
    """ """
    __tablename__ = "statuses"

"""Database entry definition module."""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///app/db/mydb.db", echo=True, future=True, connect_args={'check_same_thread': False},
                       poolclass=StaticPool)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

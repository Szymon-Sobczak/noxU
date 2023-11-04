"""NoxU database generator and seeder main entrypoint."""

from datetime import datetime
import json

from sqlalchemy.exc import IntegrityError

from . import models
from .database import engine, SessionLocal
from .models import Item, Order, OrderContent, Status, User


def initialize_table(target, connection, data):
    """Seeds database with data from specified file."""
    tablename = str(target)
    if tablename in data and len(data[tablename]) > 0:
        data = data[tablename]

        # Convert datetime strings to datetime objects
        for entry in data:
            for key, value in entry.items():
                if isinstance(value, str):
                    try:
                        entry[key] = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%fZ")
                    except ValueError:
                        pass

        connection.execute(target.insert(), data)


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    with open("app/db/seed.json", encoding="utf-8") as json_file:
        data = json.load(json_file)

    try:
        for table in [Item, Order, OrderContent, Status, User]:
            initialize_table(table.__table__, session, data)
    except IntegrityError:
        session.rollback()

    session.commit()
    session.close()

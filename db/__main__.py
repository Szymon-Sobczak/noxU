import json

from . import models
from .database import SessionLocal, engine

from .models import Status, Dough, Sauce, Cheese, Protein, Vegetable, Customer, Employee

from sqlalchemy.exc import IntegrityError


def initialize_table(target, connection, json, **kw):
    tablename = str(target)
    if tablename in json and len(json[tablename]) > 0:
        connection.execute(target.insert(), json[tablename])


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    with open('app/db/seed.json') as json_file:
        data = json.load(json_file)

    try:
        for table in [Status, Dough, Sauce, Cheese, Protein, Vegetable, Customer, Employee]:
            initialize_table(table.__table__, session, data)
    except IntegrityError:
        session.rollback()

    session.commit()
    session.close()

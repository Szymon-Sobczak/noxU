"""CRUD functions to operate on ProductionLog table from database."""
import datetime

from app.api.schemas.schemas import ProductionLog, ProductionLogCreate, ProductionLogUpdate
from app.db.models import Order, ProductionLog, User
from fastapi import HTTPException
from sqlalchemy import  desc, label
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.orm.exc import UnmappedInstanceError


def get_production_log(db: Session, log_id: int):
    """Get a single entry from the ProductionLog table using id."""
    return db.query(ProductionLog).filter(ProductionLog.log_id == log_id).first()


def get_production_log_user_name_time_interval(db: Session, user_id: int, min_timestamp: datetime, max_timestamp: datetime):
    """Get a single entry from the ProductionLog table using id."""
    query = (db.query(ProductionLog, label('order_name', Order.order_name))
             .join(Order)
             .filter(ProductionLog.user_id == user_id,
                     ProductionLog.creation_date.between(min_timestamp, max_timestamp))
             .order_by(desc(ProductionLog.creation_date))
             .all())

    result_list = [{
        "user_id": production_log.user_id,
        "order_id": production_log.order_id,
        "creation_date": production_log.creation_date,
        "log_id": production_log.log_id,
        "status": production_log.status,
        "additional_info": production_log.additional_info,
        "order_name": order_name
    } for production_log, order_name in query]

    return result_list


def get_production_log_list(db: Session):
    """Get a list of all entries from the ProductionLog table."""
    return db.query(ProductionLog).all()


def create_production_log(db: Session, production_log: ProductionLogCreate):
    """Create a single entry in the Orders table."""
    db_production_log = ProductionLog(user_id=production_log.user_id,
                                      order_id=production_log.order_id,
                                      status=production_log.status,
                                      creation_date=production_log.creation_date,
                                      additional_info=production_log.additional_info)
    try:
        db.add(db_production_log)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400,
                            detail=f"New Production Log entry is not valid.")

    return db_production_log


def update_production_log(db: Session, log_id: int, new_production_log: ProductionLogUpdate):
    """Update a single entry from the Orders table with id."""
    db_production_log = db.query(ProductionLog).filter(
        ProductionLog.log_id == log_id).first()

    try:
        update_data = new_production_log.model_dump(exclude_unset=True)
        db.query(ProductionLog).filter(ProductionLog.log_id ==
                                       log_id).update(update_data)
        db.commit()
        db.refresh(db_production_log)
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=404, detail=f"Production Log with id {log_id} not found.")
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Production Log can not be changed.")

    return db_production_log

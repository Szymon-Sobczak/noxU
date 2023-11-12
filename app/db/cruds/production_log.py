"""CRUD functions to operate on ProductionLog table from database."""

from app.api.schemas.schemas import ProductionLog, ProductionLogCreate, ProductionLogUpdate
from app.db.models import ProductionLog
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError


def get_production_log(db: Session, log_id: int):
    """Get a single entry from the ProductionLog table using id."""
    return db.query(ProductionLog).filter(ProductionLog.log_id == log_id).first()


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

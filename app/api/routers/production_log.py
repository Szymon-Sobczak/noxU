from datetime import datetime

from app.api.dependencies import get_db
from app.api.schemas.schemas import ProductionLog, ProductionLogCreate, ProductionLogUpdate
import app.db.cruds.production_log as crud
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix="/api/production_log",
                   tags=["Production Log"], responses={404: {"description": "Not found"}})


@router.post("/", response_model=ProductionLog)
async def create_order(new_production_log: ProductionLogCreate, db: Session = Depends(get_db)):
    """Route to Create a new database entry in the Production Log table."""
    return crud.create_production_log(db=db, production_log=new_production_log)


@router.get("/list", response_model=list[ProductionLog])
async def get_production_log_list(db: Session = Depends(get_db)):
    """Route to Get a list of all entries from the Production Log table."""
    return crud.get_production_log_list(db)


@router.get("/list/timeseries/{user_id}")
async def get_production_log_list(user_id: str, min_timestamp: datetime, max_timestamp: datetime,  db: Session = Depends(get_db)):
    """Route to Get a list of all entries from the Production Log table from timeinterval identified by user_name."""
    return crud.get_production_log_user_name_time_interval(db, user_id, min_timestamp, max_timestamp)


@router.get("/{log_id}", response_model=ProductionLog)
async def get_production_log(log_id: int, db: Session = Depends(get_db)):
    """Route to Get data on a single Production Log identified by id."""
    db_status = crud.get_production_log(db, log_id=log_id)
    if db_status is None:
        raise HTTPException(
            status_code=404, detail=f"Production Log with id {log_id} not found")
    return db_status


@router.put("/{order_id}")
async def update_order(order_id: int, updated_order: ProductionLogUpdate, db: Session = Depends(get_db)):
    """Route to update data on a single Production Log identified by id"""
    return crud.update_production_log(db, order_id, updated_order)

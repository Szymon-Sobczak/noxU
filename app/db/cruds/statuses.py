"""CRUD functions to operate on Statuses table from database."""

import app.api.schemas.schemas as schemas
from app.db.models import Status
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError


def get_status(db: Session, status_id: int):
    """Get a single entry from the Status table using id."""
    return db.query(Status).filter(Status.status_id == status_id).first()


def get_status_by_name(db: Session, description: str):
    """Get a single entry from the Status table using description."""
    return db.query(Status).filter(Status.description == description).first()


def get_status_list(db: Session):
    """Get a list of all entries from the Statuses table."""
    return db.query(Status).all()


def create_status(db: Session, status: schemas.StatusCreate):
    """Create a single entry from the Statuses table."""
    db_status = Status(description=status.description)

    try:
        db.add(db_status)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Status name already registered.")

    return db_status


def delete_status(db: Session, status_id: int):
    """Delete the single entry indicated by id from the Statuses table."""
    db_status = db.query(Status).filter(Status.status_id == status_id).first()

    try:
        db.delete(db_status)
        db.commit()
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=404, detail=f"Status with id {status_id} not found.")

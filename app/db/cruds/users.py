import app.api.schemas.schemas as schemas
from app.db.models import User
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError


def get_user(db: Session, user_id: int):
    """Get a single entry from the Users table using id."""
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Get a single entry from the User table using email."""
    return db.query(User).filter(User.email == email).first()


def get_users_list(db: Session):
    """Get a list of all entries from the User table."""
    return db.query(User).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Create a single entry from the Users table."""
    db_user = User(
        user_name=user.user_name,
        user_email=user.user_email,
        password=user.password,
        is_admin=user.is_admin,
        is_active=user.is_active)

    try:
        db.add(db_user)
        db.commit()
    except IntegrityError as ex:
        resp = str(ex.orig)
        detail = "Customer already registered"
        if "user_name" in resp:
            detail = "Username already registered"
        elif "user_email" in resp:
            detail = "Email already registered"
        raise HTTPException(
            status_code=400, detail=detail)

    return db_user


def delete_customer(db: Session, user_id: int):
    """Delete a single entry from the User table with id."""
    db_user = db.query(User).filter(
        User.user_id == user_id).first()

    try:
        db.delete(db_user)
        db.commit()
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=404, detail=f"Customer with {user_id} id not found.")

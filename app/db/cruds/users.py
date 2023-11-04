"""CRUD functions to operate on Users table from database."""

from app.api.schemas.schemas import User, UserCreate, UserUpdate
from app.db.models import User
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError


def get_user(db: Session, user_id: int):
    """Get a single entry from the Users table using id."""
    return db.query(User).filter(User.user_id == user_id).first()


def get_users_list(db: Session):
    """Get a list of all entries from the User table."""
    return db.query(User).all()


def create_user(db: Session, user: UserCreate):
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
        detail = "User already registered."
        if "user_name" in resp:
            detail = "Username already registered."
        elif "user_email" in resp:
            detail = "Email already registered."
        raise HTTPException(
            status_code=400, detail=detail)

    return db_user


def delete_user(db: Session, user_id: int):
    """Delete a single entry from the Users table with id."""
    db_user = db.query(User).filter(
        User.user_id == user_id).first()

    try:
        db.delete(db_user)
        is_admin_exists = db.query(User).filter(
            User.is_admin == True).count() == 0
        if is_admin_exists:
            db.rollback()
            raise HTTPException(
                status_code=404, detail=f"Once this user is removed, no administrator will remain.")
        else:
            db.commit()
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=404, detail=f"User with {user_id} id not found.")


def update_user(db: Session, user_id: int, new_user: UserUpdate):
    """Update a single entry from the Users table with id."""
    db_user = db.query(User).filter(
        User.user_id == user_id).first()

    try:
        update_data = new_user.model_dump(exclude_unset=True)
        db.query(User).filter(User.user_id ==
                              user_id).update(update_data)
        db.commit()
        db.refresh(db_user)
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=404, detail=f"User with {user_id} id not found.")
    except IntegrityError as ex:
        resp = str(ex.orig)
        detail = "User already registered."
        if "user_name" in resp:
            detail = "Username already registered."
        elif "user_email" in resp:
            detail = "Email already registered."
        raise HTTPException(
            status_code=400, detail=detail)

    return db_user

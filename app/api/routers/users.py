import app.db.cruds.users as crud
from app.api.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.api.schemas.schemas import User, UserCreate

router = APIRouter(prefix="/api/users",
                   tags=["Users"], responses={404: {"description": "Not found"}})


@router.post("/", response_model=User)
async def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    """Route to Create a new database entry in the Users table."""
    return crud.create_user(db=db, user=new_user)


@router.get("/list", response_model=list[User])
async def read_user(db: Session = Depends(get_db)):
    """Route to Get a list of all entries from the User table."""
    return crud.get_users_list(db)


@router.get("/id/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """Route to Get data on a single user identified by id."""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

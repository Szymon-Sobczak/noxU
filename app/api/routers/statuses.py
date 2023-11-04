import app.db.cruds.statuses as crud
from app.api.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.api.schemas.schemas import Status, StatusCreate

router = APIRouter(prefix="/api/statuses",
                   tags=["Statuses"], responses={404: {"description": "Not found"}})


@router.post("/", response_model=Status)
async def create_status(new_status: StatusCreate, db: Session = Depends(get_db)):
    """Route to Create a new database entry in the Statuses table."""
    return crud.create_status(db=db, status=new_status)


@router.get("/list", response_model=list[Status])
async def read_status(db: Session = Depends(get_db)):
    """Route to Get a list of all entries from the Statuses table."""
    return crud.get_status_list(db)


@router.get("/{status_id}", response_model=Status)
async def read_status(status_id: int, db: Session = Depends(get_db)):
    """Route to Get data on a single Status identified by id."""
    db_status = crud.get_status(db, status_id=status_id)
    if db_status is None:
        raise HTTPException(
            status_code=404, detail=f"Status with id {status_id} not found")
    return db_status


@router.delete("/{status_id}")
async def delete_status(status_id: int, db: Session = Depends(get_db)):
    """Route to delete data on a single Status identified by id"""
    crud.delete_status(db=db, status_id=status_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

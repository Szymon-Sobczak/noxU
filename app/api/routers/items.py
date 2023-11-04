import app.db.cruds.items as crud
from app.api.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.api.schemas.schemas import Item, ItemCreate, ItemBase


router = APIRouter(prefix="/api/items",
                   tags=["Items"], responses={404: {"description": "Not found"}})


@router.post("/", response_model=Item)
async def create_item(new_item: ItemCreate, db: Session = Depends(get_db)):
    """Route to Create a new database entry in the Items table."""
    return crud.create_item(db=db, new_item=new_item)


@router.post("/batch", response_model=list[ItemBase])
async def create_item_batch(new_items: list[ItemCreate], db: Session = Depends(get_db)):
    """Route to Create a new database entry in the Items table."""
    return crud.create_items_in_batch(db=db, new_items=new_items)


@router.get("/list", response_model=list[Item])
async def read_item_list(db: Session = Depends(get_db)):
    """Route to Get a list of all entries from the Item table."""
    return crud.get_items_list(db)


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    """Route to Get data on a single Item identified by id."""
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=404, detail=f"Item with id {item_id} not found")
    return db_item

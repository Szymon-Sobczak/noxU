import app.db.cruds.order_content as crud
from app.api.dependencies import get_db
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.api.schemas.schemas import OrderContent, OrderContentCreate, OrderContentUpdate

router = APIRouter(prefix="/api/order-content",
                   tags=["Order Content"], responses={404: {"description": "Not found"}})


@router.post("/", response_model=OrderContent)
async def create_order_content(order_content: OrderContentCreate, db: Session = Depends(get_db)):
    """Route to Create a new database entry in the OrderContent table."""
    return crud.create_order_content(db, order_content)


@router.get("/list/{order_id}", response_model=list[OrderContent])
async def read_oder_content_list_by_order_id(order_id: int, db: Session = Depends(get_db)):
    """Route to Get a list of all entries for spiecifed order_id from the OrderContent table."""
    return crud.get_order_content_list_by_order_id(db, order_id)


@router.get("/test")
async def get_order_content_details(order_id: int, db: Session = Depends(get_db)):
    """Route to Get a list of all entries for spiecifed order_id from the OrderContent table."""
    return crud.get_order_content_details(db, order_id)


@router.get("/list", response_model=list[OrderContent])
async def read_oder_content_list(db: Session = Depends(get_db)):
    """Route to Get a list of all entries from the OrderContent table."""
    return crud.get_oder_content_list(db)


@router.delete("/{order_item_id}")
async def delete_user(order_id: int, db: Session = Depends(get_db)):
    """Route to delete data on a single Order Content identified by id"""
    crud.delete_order_content(db, order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{order_item_id}")
async def update_order_content(order_id: int, update_order_content: OrderContentUpdate, db: Session = Depends(get_db)):
    """Route to update data on a single Order Content identified by id"""
    return crud.update_order_content(db, order_id, update_order_content)

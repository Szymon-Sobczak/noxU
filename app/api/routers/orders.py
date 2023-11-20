import app.db.cruds.orders as crud
from app.api.dependencies import get_db
from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session
from app.api.schemas.schemas import Order, OrderCreate, OrderUpdate, OrderWithContent

router = APIRouter(prefix="/api/orders",
                   tags=["Orders"], responses={404: {"description": "Not found"}})


@router.post("/", response_model=Order)
async def create_order(new_order: OrderCreate, db: Session = Depends(get_db)):
    """Route to Create a new database entry in the Orders table."""
    return crud.create_order(db=db, order=new_order)


@router.get("/list", response_model=list[Order])
async def read_status(db: Session = Depends(get_db)):
    """Route to Get a list of all entries from the Orders table."""
    return crud.get_oder_list(db)


@router.get("/list/ordercontet")
async def read_status(db: Session = Depends(get_db)):
    """Route to Get a list of all entries from the Orders table."""
    return crud.get_oder_list_ordercontet(db)


@router.get("/{order_id}", response_model=Order)
async def read_order(order_id: int, db: Session = Depends(get_db)):
    """Route to Get data on a single Order identified by id."""
    db_order = crud.get_oder(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(
            status_code=404, detail=f"Order with id {order_id} not found")
    return db_order


@router.delete("/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Route to delete data on a single Order identified by id"""
    crud.delete_order(db=db, order_id=order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{order_id}")
async def update_order(order_id: int, updated_order: OrderUpdate, db: Session = Depends(get_db)):
    """Route to update data on a single Order identified by id"""
    return crud.update_order(db, order_id, updated_order)

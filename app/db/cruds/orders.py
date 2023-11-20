"""CRUD functions to operate on Orders table from database."""

from app.api.schemas.schemas import Order, OrderCreate, OrderUpdate
from app.db.models import Order, OrderContent, Item
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased, joinedload, load_only
from sqlalchemy.orm.exc import UnmappedInstanceError


def get_oder(db: Session, order_id: int):
    """Get a single entry from the Orders table using id."""
    return db.query(Order).filter(Order.order_id == order_id).first()


def get_oder_by_order_name(db: Session, order_name: str):
    """Get a single entry from the Orders table using order name."""
    return db.query(Order).filter(Order.order_name == order_name).first()


def get_oder_list(db: Session):
    """Get a list of all entries from the Orders table."""
    return db.query(Order).all()


def get_oder_list_ordercontet(db: Session):
    """Get a list of all entries from the Orders with ordercontent table."""
    return db.query(Order).join(OrderContent).join(Item).options(
        joinedload(Order.order_content).joinedload(OrderContent.items)).order_by(Item.item_name).filter().all()


def create_order(db: Session, order: OrderCreate):
    """Create a single entry in the Orders table."""
    db_order = Order(order_name=order.order_name,
                     creation_date=order.creation_date)
    try:
        db.add(db_order)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400,
                            detail=f"Order with name {order.creation_date} already exists.")

    return db_order


def update_order(db: Session, order_id: int, new_order: OrderUpdate):
    """Update a single entry from the Orders table with id."""
    db_order_content = db.query(Order).filter(
        Order.order_id == order_id).first()

    try:
        update_data = new_order.model_dump(exclude_unset=True)
        db.query(Order).filter(Order.order_id ==
                               order_id).update(update_data)
        db.commit()
        db.refresh(db_order_content)
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=404, detail=f"Order Content with id {order_id} not found.")
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Order can not be changed.")

    return db_order_content


def delete_order(db: Session, order_id: int):
    """Delete the single entry indicated by id from the Orders table."""
    db_order_content = db.query(Order).filter(
        Order.order_id == order_id).first()

    try:
        db.delete(db_order_content)
        db.commit()
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=404, detail=f"Order Content with id {order_id} not found.")

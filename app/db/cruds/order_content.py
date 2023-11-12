"""CRUD functions to operate on OrderContent table from database."""

from app.api.schemas.schemas import OrderContent, OrderContentCreate, OrderContentUpdate
from app.db.models import OrderContent, Item
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError


def get_oder_content(db: Session, order_item_id: int):
    """Get a single entry from the OrderContent table using id."""
    return db.query(OrderContent).filter(OrderContent.order_item_id == order_item_id).first()


def get_oder_content_list(db: Session):
    """Get a list of all entries from the OrderContent table."""
    return db.query(OrderContent).all()


def get_order_content_list_by_order_id(db: Session, order_id: str):
    """Get a list of OrderContent entries for specified order_id."""
    return db.query(OrderContent).filter(OrderContent.order_id == order_id).all()


def get_order_content_details(db: Session, order_id: str):
    """Get a details of items of OrderContent entry for specified order_id."""
    return db.query(Item.label_number, OrderContent.quantity).join(Item).filter(OrderContent.order_id == order_id).all()


def create_order_content(db: Session, order_content: OrderContentCreate):
    """Create a single entry from the OrderContent table."""
    db_order_content = OrderContent(order_id=order_content.order_id,
                                    item_id=order_content.item_id,
                                    quantity=order_content.quantity)

    try:
        is_order_content_exists = db.query(OrderContent).filter(
            OrderContent.order_id == order_content.order_id,
            OrderContent.item_id == order_content.item_id).count() == 0
        if is_order_content_exists:
            db.add(db_order_content)
            db.commit()
        else:
            db.rollback()
            raise HTTPException(
                status_code=400, detail=f"Order Content already exists.")
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Order Content can not be created for specified order.")

    return db_order_content


def update_order_content(db: Session, order_item_id: int, new_order_content: OrderContentUpdate):
    """Update a single entry from the Users table with id."""
    db_order_content = db.query(OrderContent).filter(
        OrderContent.order_item_id == order_item_id).first()

    try:
        update_data = new_order_content.model_dump(exclude_unset=True)
        db.query(OrderContent).filter(OrderContent.order_item_id ==
                                      order_item_id).update(update_data)

        is_order_content_multiplies = db.query(OrderContent).filter(
            OrderContent.order_id == new_order_content.order_id,
            OrderContent.item_id == new_order_content.item_id).count() != 1
        if is_order_content_multiplies:
            db.rollback()
            raise HTTPException(
                status_code=400, detail=f"Order Content already exists.")
        else:
            db.commit()
            db.refresh(db_order_content)
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=404, detail=f"Order Content with {order_item_id} id not found.")
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Order Content can not be created.")

    return db_order_content


def delete_order_content(db: Session, order_item_id: int):
    """Delete the single entry indicated by id from the OrderContent table."""
    db_order_content = db.query(OrderContent).filter(
        OrderContent.order_item_id == order_item_id).first()

    try:
        db.delete(db_order_content)
        db.commit()
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=404, detail=f"Order Content with id {order_item_id} not found.")

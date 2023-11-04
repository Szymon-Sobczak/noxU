"""CRUD functions to operate on Items table from database."""

from app.api.schemas.schemas import Item, ItemCreate
from app.db.models import Item
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError


def get_item(db: Session, item_id: int):
    """Get a single entry from the item table using id."""
    return db.query(Item).filter(Item.item_id == item_id).first()


def get_items_list(db: Session):
    """Get a list of all entries from the Items table."""
    return db.query(Item).all()


def create_item(new_item: ItemCreate, db: Session):
    """Create a single entry in the Item table."""
    db_item = Item(
        item_name=new_item.item_name,
        label_number=new_item.label_number,
    )

    try:
        db.add(db_item)
        db.commit()
    except IntegrityError as ex:
        db.rollback()
        resp = str(ex.orig)
        detail = "Item already exists."
        if "item_name" in resp:
            detail = "Item name already registered."
        elif "label_number" in resp:
            detail = "Item label number already registered."
        raise HTTPException(
            status_code=400, detail=detail)

    return db_item


def create_items_in_batch(new_items: list[ItemCreate], db: Session):
    """Create a batch of entries in the Item table."""
    db_items = [Item(
        item_name=item.item_name,
        label_number=item.label_number,
    ) for item in new_items]

    try:
        db.bulk_save_objects(db_items)
        db.commit()
    except IntegrityError as ex:
        db.rollback()
        resp = str(ex.orig)
        detail = "Item contained in batch already exists."
        if "item_name" in resp:
            detail = "Item name already registered."
        elif "label_number" in resp:
            detail = "Item label number already registered."
        raise HTTPException(
            status_code=400, detail=detail)

    return db_items

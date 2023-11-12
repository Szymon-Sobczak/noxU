from app.api.dependencies import get_db
from app.api.schemas.schemas import Item, ItemBase, ItemCreate
from fastapi import APIRouter, Depends, HTTPException, Response, status
import qrcode
from sqlalchemy.orm import Session
from io import BytesIO

from app.db.cruds.orders import get_oder
router = APIRouter(prefix="/api/qrcodes",
                   tags=["Qrcodes"], responses={404: {"description": "Not found"}})


@router.get("/generate/{order_id}")
async def generate_qrcode(order_id: str, db: Session = Depends(get_db)):
    """Route to generate QR code containing order name."""
    db_order = get_oder(db, order_id)
    if db_order is None:
        raise HTTPException(
            status_code=404, detail=f"Order with id {order_id} not found.")
    try:
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2)

        qr.add_data(db_order.order_name)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        b = BytesIO()
        img.save(b, 'jpeg')
        im_bytes = b.getvalue()

    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Generating QRCode is not possible due to error: {error}.")

    return Response(content=im_bytes, media_type="image/png")

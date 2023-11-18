from datetime import datetime
from io import BytesIO
import json
from pathlib import Path

from PIL import Image
from app.api.dependencies import get_db, read_yolo_model_from_file
from app.api.schemas.schemas import ProductionLogCreate
from app.db.cruds.orders import get_oder_by_order_name
from app.db.cruds.order_content import get_order_content_details
from app.db.cruds.production_log import create_production_log
from app.db.models import BasicStatuses
from app.yolo_model.model_utils import read_qr_codes, evaluate_order_content, handle_order_not_found, handle_wrong_qr
from fastapi import APIRouter, Depends, HTTPException, Response, status, UploadFile
from sqlalchemy.orm import Session
import ultralytics


router = APIRouter(prefix="/api/analyse",
                   tags=["Analyse"], responses={404: {"description": "Not found"}})

model = read_yolo_model_from_file(Path("app/yolo_model/yolo_model.pt"))

# REMEMBER TO ADD LIBGl1 from APT apt-get install ffmpeg libsm6 libxext6  -y


@router.post("/detect/")
async def detect_objects(new_image: UploadFile, user_id: int, db: Session = Depends(get_db)):
    """ """
    file_contents = await new_image.read()
    image = Image.open(BytesIO(file_contents)).convert("RGB")

    qr_codes = read_qr_codes(image)

    if len(qr_codes) != 1 or None in qr_codes:
        handle_wrong_qr(db, user_id)

    order_name = qr_codes[0]

    db_order = get_oder_by_order_name(db, order_name)
    if db_order is None:
        handle_order_not_found(db, user_id, order_name)

    order_content = get_order_content_details(db, db_order.order_id)
    if order_content is None:
        raise HTTPException(status_code=404,
                            detail=f"Order content for order with {order_content} id not found")

    detections = model(image, conf=0.6)
    detection_dict = json.loads(detections[0].tojson())

    detection_result, detection_report = evaluate_order_content(detection_dict,
                                                                order_content)

    # THINK ABOUT BETTER HANDLING IF THE TRAY IS INTENTIONALLY EMPTY!
    detection_status = BasicStatuses.NOK
    if not any(item["status"] == "nok" for item in detection_dict) and len(detection_result) != 0:
        detection_status = BasicStatuses.OK

    if len(detection_result) == 0 and len(order_content) == 0:
        detection_status = BasicStatuses.OK

    create_production_log(db, ProductionLogCreate(user_id=user_id,
                                                  order_id=db_order.order_id,
                                                  status=detection_status,
                                                  creation_date=datetime.now(),
                                                  additional_info=None))
    # HANDLE ERROR CODES FOR OK AND NOK!
    analysis = {"detection_result": detection_status,
                "detection_report": detection_report}
    return {"analysis": analysis, "detection_result": detection_result}

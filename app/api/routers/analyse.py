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
from app.yolo_model.model_utils import read_qr_codes
from fastapi import APIRouter, Depends, HTTPException, Response, status, UploadFile
from sqlalchemy.orm import Session
import ultralytics


router = APIRouter(prefix="/api/analyse",
                   tags=["Analyse"], responses={404: {"description": "Not found"}})

model = read_yolo_model_from_file(Path("app/yolo_model/yolo_model.pt"))

# REMEMBER TO ADD LIBGl1 from APT apt-get install ffmpeg libsm6 libxext6  -y


@router.post("/detect/")
async def detect_objects(new_image: UploadFile, user_id: str, db: Session = Depends(get_db)):
    file_contents = await new_image.read()
    image = Image.open(BytesIO(file_contents)).convert("RGB")

    qr_codes = read_qr_codes(image)
    print(qr_codes)
    if len(qr_codes) != 1 or None in qr_codes:
        # create_production_log(db, ProductionLogCreate(user_id=user_id,
        #                                               order_id=None,
        #                                               status=BasicStatuses.WRONG_QR,
        #                                               creation_date=datetime.now(),
        #                                               additional_info=None))
        raise HTTPException(status_code=404,
                            detail=f"No or wrong number of QR codes in the image.")

    order_name = qr_codes[0]
    print(order_name)
    db_order = get_oder_by_order_name(db, order_name)
    if db_order is None:
        # create_production_log(db, ProductionLogCreate(user_id=user_id,
        #                                               order_id=None,
        #                                               status=BasicStatuses.WRONG_QR,
        #                                               creation_date=datetime.now(),
        #                                               additional_info=None))
        raise HTTPException(status_code=404,
                            detail=f"Order with name {order_name} not found")

    order_content = get_order_content_details(db, db_order.order_id)
    if order_content is None:
        raise HTTPException(status_code=404,
                            detail=f"Order content for order with {order_content} id not found")
    # order_content_list = [{"order_name": content[0].order_name, "label_number": content[2], "item_id": content[1].item_id, "quantity": content[1].quantity}
    #                       for content in order_content]
    print("*"*50)
    print(order_content)
    print("*"*50)
    # order_content_list = [content.__dict__
    #                       for content in db_order]
    # for order, order_content, label_number in db_order:
    #     print(
    #         f"Order: {order.order_name}, OrderContent ID: {order_content.order_item_id}, Item Label Number: {label_number}"
    #     )
    # print("*"*50)
    # print(order_content_list)
    # print("*"*50)

    detections = model(image, conf=0.6)
    detection_dict = json.loads(detections[0].tojson())
    print(detection_dict)

    class_counts = {}
    for item in detection_dict:
        class_counts[item['class']] = class_counts.get(item['class'], 0) + 1

    for item in detection_dict:
        for element in order_content:
            if item['class'] == element[0] and class_counts[item['class']] == element[1]:
                item['status'] = 'ok'
                break
            else:
                item['status'] = 'nok'

    # result = json.dumps(order_content_list)
    return detection_dict
    b = BytesIO()
    image.save(b, 'jpeg')
    im_bytes = b.getvalue()
    print(order_content_list)
    return Response(content=im_bytes, media_type="image/jpeg")


# @router.post("/detect/")
# async def detect_objects(new_image: UploadFile):

#     file_contents = await new_image.read()
#     image = Image.open(BytesIO(file_contents)).convert("RGB")
#     detections = model(image)  # Perform object detection
#     detection = detections[0].tojson()
#     print(detection)
#     # im = Image.fromarray(im_array[..., ::-1])
#     # b = BytesIO()
#     # im.save(b, 'jpeg')
#     # im_bytes = b.getvalue()

#     my_dict = {
#         "name": "aaa"
#     }
#     x, y, x2, y2 = (1195.9180908203125, 630.4423828125,
#                     1445.0205078125, 886.781494140625)

#     draw = ImageDraw.Draw(image)
#     font_size = int(min(x2-x, y2-y) / 5)  # Adjust the multiplier as needed
#     font = ImageFont.load_default().font_variant(size=font_size)
#     draw.rectangle([(x, y), (x2, y2)], outline="green", width=8)
#     position = (x, y-font_size)
#     # Draw the filled rectangle as the background
#     left, top, right, bottom = draw.textbbox(
#         position, "Transistor", font=font)
#     draw.rectangle((left, top-5, right+5, bottom+5), fill="green")
#     draw.text(position, "Transistor", font=font, fill="white")

#     b = BytesIO()
#     image.save(b, 'jpeg')
#     im_bytes = b.getvalue()
#     # im_base64 = base64.b64encode(im_bytes).decode('utf-8')
#     # im_bytes = base64.b64decode(im_base64)

#     return Response(content=im_bytes, headers=my_dict, media_type="image/jpeg")

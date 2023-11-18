"""Utils to help analyze images sent for detection"""

from datetime import datetime
from typing import List

from PIL import Image
from app.api.schemas.schemas import ProductionLogCreate
from app.db.models import BasicStatuses
import cv2
from app.db.cruds.production_log import create_production_log
from fastapi import HTTPException
import numpy as np
from qreader import QReader


def read_qr_codes(source: Image) -> List[str]:
    """Reads qr codes present in the given source image."""
    decoded_qrs: List[str] = []

    try:
        image_np = np.array(source)
        image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        qreader = QReader()
        decoded_qrs = qreader.detect_and_decode(image=image)
    except cv2.error:
        return None

    return decoded_qrs


def evaluate_order_content(detection: dict, order_content: dict) -> dict:
    class_counts = {}
    for item in detection:
        class_counts[item['class']] = class_counts.get(item['class'], 0) + 1

    result_detection = detection
    detection_report = {}

    for item in result_detection:
        for element in order_content:
            if item['class'] == element[0] and class_counts[item['class']] == element[1]:
                item['status'] = 'ok'
                detection_report[item['name']] = 'Ok.'
                break
            else:
                item['status'] = 'nok'
                if item['class'] != element[0] and class_counts[item['class']] == element[1]:
                    detection_report[item['name']] = 'Wrong component.'
                elif item['class'] == element[0] and class_counts[item['class']] > element[1]:
                    detection_report[item['name']] = 'Too many components.'
                elif item['class'] == element[0] and class_counts[item['class']] < element[1]:
                    detection_report[item['name']] = 'Too few components.'

    return result_detection, detection_report


def handle_wrong_qr(db, user_id):
    create_production_log(db, ProductionLogCreate(user_id=user_id,
                                                  order_id=None,
                                                  status=BasicStatuses.WRONG_QR,
                                                  creation_date=datetime.now(),
                                                  additional_info=None))
    raise HTTPException(status_code=404,
                        detail=f"No or wrong number of QR codes in the image.")


def handle_order_not_found(db, user_id, order_name):
    create_production_log(db, ProductionLogCreate(user_id=user_id,
                                                  order_id=None,
                                                  status=BasicStatuses.WRONG_ORDER,
                                                  creation_date=datetime.now(),
                                                  additional_info=None))
    raise HTTPException(
        status_code=404, detail=f"Order with name {order_name} not found.")

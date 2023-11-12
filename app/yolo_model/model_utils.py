"""Utils to help analyze images sent for detection"""

from PIL import Image
from qreader import QReader
import cv2
import numpy as np
from typing import List


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

    for item in result_detection:
        for element in order_content:
            if item['class'] == element[0] and class_counts[item['class']] == element[1]:
                item['status'] = 'ok'
                break
            else:
                item['status'] = 'nok'

    return result_detection


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
        status_code=404, detail=f"Order with name {order_name} not found")

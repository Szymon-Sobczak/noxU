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

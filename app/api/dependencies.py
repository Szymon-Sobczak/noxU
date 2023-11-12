"""Dependencies module for NoxU API."""

from app.db.database import SessionLocal
from ultralytics import YOLO
from pathlib import Path


def get_db():
    """Yields Database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def read_yolo_model_from_file(yolo_model_path: Path):
    """Loads ultralytics YOLO model for object detection."""
    if not yolo_model_path.is_file():
        raise FileNotFoundError(
            f"Yolo model not found at path: {yolo_model_path}")
    try:
        yolo_model = YOLO(yolo_model_path)
    except Exception as error:
        raise Exception(f"Error occured during loading YOLO model {error}.")
    return yolo_model


def get_yolo_model():
    """Yields ultralytics YOLO model."""
    yolo_model = read_yolo_model_from_file()
    try:
        yield yolo_model
    except Exception:
        yield None

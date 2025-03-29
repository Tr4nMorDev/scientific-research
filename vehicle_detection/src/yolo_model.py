from ultralytics import YOLO
from .config import YOLO_MODEL_PATH

def load_yolo_model():
    """Load mô hình YOLO"""
    return YOLO(YOLO_MODEL_PATH)

yolo_model = load_yolo_model()

from ultralytics import YOLO

def load_yolo_model():
    """Load mô hình YOLO"""
    return YOLO("yolov8n.pt")

yolo_model = load_yolo_model()

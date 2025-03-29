import os

# Lấy đường dẫn gốc của project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Đường dẫn mô hình YOLO
YOLO_MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov8n.pt")

# Đường dẫn video đầu vào & đầu ra
INPUT_VIDEO_PATH = os.path.join(BASE_DIR, "data", "input", "VDCame1.mp4")
OUTPUT_VIDEO_PATH = os.path.join(BASE_DIR, "data", "output", "output_video.mp4")

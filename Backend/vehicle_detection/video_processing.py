import cv2
import numpy as np
from yolo_model import yolo_model
from config import INPUT_VIDEO_PATH, OUTPUT_VIDEO_PATH

def process_video():
    """Xử lý video, nhận diện xe cộ"""
    cap = cv2.VideoCapture("C:/NCKH/Backend/vehicle_detection/input/VDCame1.mp4")
    if not cap.isOpened():
        print("Lỗi: Không thể mở video!")
        return
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Nhận diện xe trong từng khung hình
        results = yolo_model(frame)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())

                # Vẽ bounding box nếu phát hiện là xe (car, bus, truck)
                if cls in [2, 5, 7] and conf > 0.3:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()
    print("✔ Video đã xử lý xong!")


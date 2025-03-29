# Vehicle Detection System

Hệ thống nhận diện xe cộ sử dụng YOLOv8.

## Cấu trúc thư mục

```
vehicle_detection/
├── models/                 # Chứa các file model
│   └── yolov8n.pt
├── src/                    # Mã nguồn
│   ├── __init__.py
│   ├── config.py
│   ├── yolo_model.py
│   └── video_processing.py
├── data/                   # Dữ liệu
│   ├── input/             # Video đầu vào
│   └── output/            # Video đầu ra
├── requirements.txt
└── main.py
```

## Cài đặt

1. Cài đặt Python 3.8 trở lên
2. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## Sử dụng

1. Đặt video cần xử lý vào thư mục `data/input/`
2. Chạy chương trình:

```bash
python main.py
```

3. Video đã xử lý sẽ được lưu trong thư mục `data/output/`

## Lưu ý

- Đảm bảo video đầu vào có định dạng MP4
- Hệ thống có thể phát hiện các loại xe: ô tô, xe buýt, xe tải
- Ngưỡng tin cậy mặc định: 0.3

# Vehicle Detection System

Hệ thống nhận diện xe cộ sử dụng YOLOv8.

## Cấu trúc thư mục

```
project_root/
├── .github/
│ └── workflows/
│ └── python-test.yml # GitHub Actions workflow
├── vehicle_detection/
│ ├── init.py
│ ├── server.py # Flask server
│ ├── src/
│ │ ├── init.py
│ │ └── yolo_model.py # YOLO model implementation
│ ├── static/ # Static files cho frontend
│ └── templates/ # HTML templates
├── frontend/ # Frontend code
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md
```

## Cài đặt

1. Tạo môi trường ảo:

```bash
python -m venv venv
```

2. Kích hoạt môi trường ảo:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

1. Đảm bảo đang trong môi trường ảo (venv)

2. Chạy server:

```bash
python vehicle_detection/server.py
```

## Công nghệ sử dụng

- Python
- Flask
- YOLO
- OpenCV
- portgresql
- websocket
- [các công nghệ khác]

## Tính năng

- [Liệt kê các tính năng chính]

## Đóng góp

[Hướng dẫn đóng góp cho dự án]

## License

[Thông tin về license]

## Lưu ý

- Đảm bảo video đầu vào có định dạng MP4
- Hệ thống có thể phát hiện các loại xe: ô tô, xe buýt, xe tải
- Ngưỡng tin cậy mặc định: 0.3

vehicle_detection/
├── __init__.py
├── server.py
├── config/
│   ├── __init__.py
│   ├── settings.py          # Các config và đường dẫn
│   └── database.py         # Cấu hình database
└─ src/
  ├── __init__.py
  ├── entity/             # Đổi tên từ entities sang entity
  │   ├── __init__.py
  │   ├── base.py        # Base model
  │   └── traffic.py     # Gộp các model liên quan traffic
  ├── service/           # Đổi tên từ services sang service
  │   ├── __init__.py
  │   └── traffic_service.py
  └── model/             # Đổi tên từ models sang model
      ├── __init__.py
      ├── yolo_model.py
      └── yolov8n.pt     # File model
from flask import Flask 
from flask_cors import CORS
from flask_socketio import SocketIO
from src.yolo_model import yolo_model
from PIL import Image
from dotenv import load_dotenv
import os
from pathlib import Path
from queue import Queue
from config.database import SessionLocal, Base, engine
from src.video_processing import process_video  # Import từ module mới

# Lấy đường dẫn tới file .env ở thư mục gốc
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

app = Flask(__name__)
CORS(app)

# Lấy giá trị từ .env với giá trị mặc định
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Khởi tạo Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == '__main__':
    # Chạy server
    print(f"Starting server on port {PORT}...")
    socketio.run(app, 
                 host=HOST, 
                 port=PORT, 
                 debug=DEBUG) 
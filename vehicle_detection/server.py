from flask import Flask, jsonify, render_template, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
from src.yolo_model import yolo_model
import base64
import io
from PIL import Image
import threading
import time
import os
import json
from queue import Queue

app = Flask(__name__)
CORS(app)

# Khởi tạo Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")

# Biến toàn cục để kiểm soát luồng video
camera_threads = {}
camera_status = {}
active_camera = None  # Camera đang được xem

class CameraProcessor:
    def __init__(self, camera_id, video_path):
        self.camera_id = camera_id
        self.video_path = video_path
        self.running = False
        self.thread = None
        self.cap = None

    def process_frame(self, frame):
        """Xử lý một frame và trả về kết quả nhận diện"""
        try:
            if frame is None:
                return None, []
                
            # Giữ nguyên kích thước frame gốc
            frame = frame.copy()
            
            # Nhận diện xe
            results = yolo_model(frame)
            detections = []
            
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0].item()
                    cls = int(box.cls[0].item())
                    
                    # Chỉ lấy các xe (car, bus, truck) với độ tin cậy > 0.3
                    if cls in [2, 5, 7] and conf > 0.3:
                        detections.append({
                            'bbox': [x1, y1, x2, y2],
                            'confidence': conf,
                            'class': cls
                        })
                        
                        # Vẽ bounding box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            return frame, detections
        except Exception as e:
            print(f"Lỗi xử lý frame camera {self.camera_id}: {str(e)}")
            return None, []

    def capture_frames(self):
        """Thread để đọc frames từ video"""
        try:
            self.cap = cv2.VideoCapture(self.video_path)
            
            if not self.cap.isOpened():
                print(f"Lỗi: Không thể mở file video cho camera {self.camera_id}")
                return
            
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            frame_delay = 1 / fps
            frame_count = 0
            
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                    
                if frame_count % 2 == 0:  # Xử lý mỗi 2 frame
                    processed_frame, detections = self.process_frame(frame)
                    
                    if processed_frame is not None and self.camera_id == active_camera:
                        _, buffer = cv2.imencode('.jpg', processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                        frame_base64 = base64.b64encode(buffer).decode('utf-8')
                        
                        socketio.emit('camera_update', {
                            'camera_id': self.camera_id,
                            'frame': frame_base64,
                            'detections': detections
                        })
                
                frame_count += 1
                time.sleep(frame_delay)
            
            if self.cap:
                self.cap.release()
        except Exception as e:
            print(f"Lỗi trong capture_frames camera {self.camera_id}: {str(e)}")
            if self.cap:
                self.cap.release()

    def start(self):
        """Bắt đầu xử lý camera"""
        if self.thread and self.thread.is_alive():
            return False
        
        self.running = True
        self.thread = threading.Thread(target=self.capture_frames)
        self.thread.start()
        return True

    def stop(self):
        """Dừng xử lý camera"""
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None
        if self.cap:
            self.cap.release()
            self.cap = None

@app.route('/')
def index():
    """Trang chủ hiển thị video từ camera"""
    return render_template('index.html')

@app.route('/api/cameras', methods=['GET'])
def get_cameras():
    """API để lấy danh sách camera"""
    video_path = os.path.join('data', 'input', 'VDCame1.mp4')
    if not os.path.exists(video_path):
        print(f"Lỗi: Không tìm thấy file video tại {video_path}")
        return jsonify({'error': 'Video file not found'}), 404
        
    cameras = [
        {'id': 1, 'name': 'Camera 1', 'url': video_path},
        {'id': 2, 'name': 'Camera 2', 'url': video_path},
        {'id': 3, 'name': 'Camera 3', 'url': video_path},
        {'id': 4, 'name': 'Camera 4', 'url': video_path}
    ]
    return jsonify({'cameras': cameras})

@app.route('/api/camera/<int:camera_id>/start', methods=['POST'])
def start_camera(camera_id):
    """API để bắt đầu camera"""
    if camera_id in camera_threads:
        return jsonify({'error': 'Camera đang chạy'}), 400
    
    cameras = get_cameras().json['cameras']
    camera_info = next((c for c in cameras if c['id'] == camera_id), None)
    
    if not camera_info:
        return jsonify({'error': 'Camera không tồn tại'}), 404
    
    try:
        processor = CameraProcessor(camera_id, camera_info['url'])
        if processor.start():
            camera_threads[camera_id] = processor
            camera_status[camera_id] = True
            return jsonify({'message': f'Camera {camera_id} đã bắt đầu'})
    except Exception as e:
        print(f"Lỗi khi khởi tạo camera {camera_id}: {str(e)}")
        return jsonify({'error': f'Lỗi khi khởi tạo camera: {str(e)}'}), 500
    
    return jsonify({'error': 'Không thể bắt đầu camera'}), 500

@app.route('/api/camera/<int:camera_id>/stop', methods=['POST'])
def stop_camera(camera_id):
    """API để dừng camera"""
    if camera_id not in camera_threads:
        return jsonify({'error': 'Camera không tồn tại'}), 404
    
    processor = camera_threads[camera_id]
    processor.stop()
    del camera_threads[camera_id]
    camera_status[camera_id] = False
    return jsonify({'message': f'Camera {camera_id} đã dừng'})

@app.route('/api/camera/<int:camera_id>/status', methods=['GET'])
def get_camera_status(camera_id):
    """API để lấy trạng thái camera"""
    is_running = camera_status.get(camera_id, False)
    return jsonify({
        'camera_id': camera_id,
        'is_running': is_running
    })

@app.route('/api/camera/<int:camera_id>/set_active', methods=['POST'])
def set_active_camera(camera_id):
    """API để đặt camera đang được xem"""
    global active_camera
    active_camera = camera_id
    return jsonify({'message': f'Camera {camera_id} đã được đặt làm camera chính'})

@app.route('/api/camera/<int:camera_id>/video_feed')
def video_feed(camera_id):
    """API để stream video trực tiếp"""
    try:
        if camera_id not in camera_threads:
            print(f"Camera {camera_id} chưa được khởi tạo")
            return jsonify({'error': 'Camera không tồn tại'}), 404

        processor = camera_threads[camera_id]
        
        # Kiểm tra và khởi tạo video capture nếu cần
        if not processor.cap:
            processor.cap = cv2.VideoCapture(processor.video_path)
            if not processor.cap.isOpened():
                print(f"Không thể mở file video cho camera {camera_id}")
                return jsonify({'error': 'Không thể mở file video'}), 500

        def generate():
            while True:
                try:
                    ret, frame = processor.cap.read()
                    if not ret:
                        processor.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue

                    processed_frame, _ = processor.process_frame(frame)
                    if processed_frame is not None:
                        _, buffer = cv2.imencode('.jpg', processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                except Exception as e:
                    print(f"Lỗi xử lý frame camera {camera_id}: {str(e)}")
                    continue

        return Response(generate(),
                       mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Lỗi trong video_feed camera {camera_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Chạy server
    print("Starting server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 
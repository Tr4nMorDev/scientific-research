from flask import Flask, Response, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
from vehicle_detection.config.database import init_db
from vehicle_detection.config.settings import APP_CONFIG
import os
import cv2
from .src.traffic_detection import TrafficDetector

# Initialize Flask app
app = Flask(__name__)

# Apply configurations
if APP_CONFIG['cors_enabled']:
    CORS(app)

socketio = SocketIO(app)

# Initialize database
init_db(app)

# Initialize traffic detector
detector = TrafficDetector()

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video to start
            continue
            
        # Process frame with YOLO
        results = detector.detect(frame)
        
        # Draw bounding boxes and count vehicles
        vehicle_count = results['vehicle_count']
        for vehicle in results['vehicles']:
            x1, y1, x2, y2 = vehicle['bbox']
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        
        # Add vehicle count text
        cv2.putText(frame, f'Vehicles: {vehicle_count}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    video_path = os.path.join(APP_CONFIG['videos_folder'], 'traffic.mp4')
    return Response(generate_frames(video_path),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/videos/<path:filename>')
def serve_video(filename):
    try:
        return send_from_directory(
            APP_CONFIG['videos_folder'],
            filename,
            mimetype='video/mp4',
            as_attachment=False
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/traffic')
def get_traffic_data():
    try:
        points = detector.get_all_points_status()
        print("Traffic points:", points)  # Debug log
        return jsonify(points)
    except Exception as e:
        print(f"Error getting traffic data: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"Starting server on {APP_CONFIG['host']}:{APP_CONFIG['port']}...")
    socketio.run(
        app,
        host=APP_CONFIG['host'],
        port=APP_CONFIG['port'],
        debug=APP_CONFIG['debug']
    )
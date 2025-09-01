"""
Remote streaming server for drowning detection system.
Allows viewing webcam feed and alerts from other devices.
"""
import cv2
import json
import threading
import time
from flask import Flask, Response, render_template, jsonify
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.drowning_detector import DrowningDetector
from src.alert_system import AlertSystem

app = Flask(__name__)

class RemoteStreamingServer:
    def __init__(self, camera_source=0, host='0.0.0.0', port=5000):
        """
        Initialize remote streaming server.
        
        Args:
            camera_source: Camera index or video file path
            host: Server host (0.0.0.0 for all interfaces)
            port: Server port
        """
        self.camera_source = camera_source
        self.host = host
        self.port = port
        
        # Initialize components
        self.detector = DrowningDetector()
        self.alert_system = AlertSystem()
        
        # Load model
        print("Loading YOLO model...")
        self.detector.load_model()
        print("✅ Model loaded successfully!")
        
        # Camera and streaming
        self.camera = None
        self.frame = None
        self.detection_results = []
        self.latest_alert = None
        
        # Threading
        self.streaming = False
        self.camera_thread = None
        
    def initialize_camera(self):
        """Initialize camera capture."""
        self.camera = cv2.VideoCapture(self.camera_source)
        if not self.camera.isOpened():
            raise RuntimeError(f"Failed to open camera source: {self.camera_source}")
        
        # Set camera properties for better performance
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera.set(cv2.CAP_PROP_FPS, 30)
        
        print(f"✅ Camera initialized: {self.camera_source}")
    
    def process_frame(self):
        """Process camera frames in a separate thread."""
        detection_history = []
        
        while self.streaming:
            ret, frame = self.camera.read()
            if not ret:
                print("❌ Failed to read frame from camera")
                break
            
            # Run detection
            detections = self.detector.predict_frame(frame)
            
            # Draw detections on frame
            annotated_frame = frame.copy()
            for det in detections:
                if det['name'] == 'person':  # Only process people
                    x1, y1, x2, y2 = map(int, det['bbox'])
                    confidence = det['confidence']
                    
                    # Draw bounding box
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, f"Person {confidence:.2f}", 
                              (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Simple frame analysis for drowning detection
            frame_analysis = {
                'timestamp': time.time(),
                'person_detected': any(d['name'] == 'person' for d in detections),
                'person_count': sum(1 for d in detections if d['name'] == 'person'),
                'movement_speed': 0.1,  # Placeholder
                'posture_vertical': False,  # Placeholder
                'head_underwater': False,  # Placeholder
                'movement_erratic': False,  # Placeholder
            }
            
            detection_history.append(frame_analysis)
            if len(detection_history) > 750:  # Keep last 30 seconds at 25fps
                detection_history.pop(0)
            
            # Check for drowning patterns
            if len(detection_history) > 125:  # After 5 seconds
                drowning_analysis = self.detector.analyze_drowning_patterns(detection_history)
                
                if drowning_analysis['alert_level'] != 'none':
                    # Trigger alert
                    alert_triggered = self.alert_system.trigger_alert(drowning_analysis, frame)
                    if alert_triggered:
                        self.latest_alert = {
                            'timestamp': datetime.now().isoformat(),
                            'alert_level': drowning_analysis['alert_level'],
                            'confidence': drowning_analysis['confidence'],
                            'reasons': drowning_analysis['reasons']
                        }
                        print(f"🚨 ALERT: {drowning_analysis['alert_level']} - {drowning_analysis['confidence']:.2%}")
            
            # Store current frame and results
            self.frame = annotated_frame
            self.detection_results = detections
            
            time.sleep(0.033)  # ~30 FPS
    
    def generate_frames(self):
        """Generate frames for streaming."""
        while True:
            if self.frame is not None:
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', self.frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.033)  # ~30 FPS
    
    def start_streaming(self):
        """Start the streaming server."""
        try:
            self.initialize_camera()
            self.streaming = True
            
            # Start camera processing thread
            self.camera_thread = threading.Thread(target=self.process_frame)
            self.camera_thread.daemon = True
            self.camera_thread.start()
            
            print(f"🌐 Starting streaming server on {self.host}:{self.port}")
            print(f"📹 Camera source: {self.camera_source}")
            print(f"🔗 Access from other devices: http://{self.get_local_ip()}:{self.port}")
            print("Press Ctrl+C to stop")
            
            app.run(host=self.host, port=self.port, debug=False, threaded=True)
            
        except KeyboardInterrupt:
            print("\n🛑 Stopping streaming server...")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.stop_streaming()
    
    def stop_streaming(self):
        """Stop streaming and cleanup."""
        self.streaming = False
        if self.camera:
            self.camera.release()
        print("✅ Streaming stopped")
    
    def get_local_ip(self):
        """Get local IP address."""
        import socket
        try:
            # Connect to a remote address to get local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return "localhost"

# Global server instance
server = None

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    if server:
        return Response(server.generate_frames(),
                       mimetype='multipart/x-mixed-replace; boundary=frame')
    return "Server not initialized", 500

@app.route('/api/status')
def get_status():
    """Get current system status."""
    if server:
        return jsonify({
            'streaming': server.streaming,
            'detections': len(server.detection_results),
            'latest_alert': server.latest_alert,
            'timestamp': datetime.now().isoformat()
        })
    return jsonify({'error': 'Server not initialized'}), 500

@app.route('/api/detections')
def get_detections():
    """Get current detection results."""
    if server:
        return jsonify({
            'detections': server.detection_results,
            'timestamp': datetime.now().isoformat()
        })
    return jsonify({'error': 'Server not initialized'}), 500

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Remote Drowning Detection Streaming Server')
    parser.add_argument('--source', '-s', default=0, help='Camera source (0 for webcam, or video file path)')
    parser.add_argument('--host', default='0.0.0.0', help='Server host (0.0.0.0 for all interfaces)')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Server port')
    
    args = parser.parse_args()
    
    # Convert source to int if it's a number
    try:
        camera_source = int(args.source)
    except ValueError:
        camera_source = args.source
    
    server = RemoteStreamingServer(camera_source, args.host, args.port)
    server.start_streaming()

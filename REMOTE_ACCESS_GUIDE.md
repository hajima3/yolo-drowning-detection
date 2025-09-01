# 🏊‍♂️ Remote Access Setup Guide

This guide shows you how to duplicate the drowning detection system to other devices and access it remotely.

## 📥 Cloning to Another Device

### Step 1: Clone the Repository
```bash
git clone https://github.com/hajima3/yolo-drowning-detection.git
cd yolo-drowning-detection
```

### Step 2: Install Dependencies
**On Windows:**
```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install packages
python -m pip install -r requirements.txt
```

**On Linux/Mac:**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Test Installation
```bash
python -c "from ultralytics import YOLO; model=YOLO('yolov8n.pt'); print('✅ Setup complete!')"
```

## 🌐 Remote Webcam Streaming

### Start the Remote Streaming Server

**Option 1: Basic webcam streaming**
```bash
python src/streaming_server.py --source 0 --port 5000
```

**Option 2: Specific camera or video file**
```bash
# Use specific camera index
python src/streaming_server.py --source 1 --port 5000

# Use video file
python src/streaming_server.py --source "path/to/video.mp4" --port 5000

# Use IP camera (RTSP)
python src/streaming_server.py --source "rtsp://camera_ip/stream" --port 5000
```

### Access from Other Devices

1. **Find your server IP address:**
   - The server will display: `Access from other devices: http://YOUR_IP:5000`
   - Or check manually:
     ```bash
     # Windows
     ipconfig
     
     # Linux/Mac
     ifconfig
     ```

2. **Open in browser on any device:**
   ```
   http://YOUR_SERVER_IP:5000
   ```
   
   Examples:
   - `http://192.168.1.100:5000` (local network)
   - `http://laptop.local:5000` (if using hostname)

### 📱 Access from Mobile Devices

1. Connect your phone/tablet to the same WiFi network
2. Open browser and navigate to: `http://SERVER_IP:5000`
3. The dashboard is mobile-responsive and will work on any device

## 🔧 Advanced Configuration

### Custom Port and Host
```bash
# Listen on all interfaces, custom port
python src/streaming_server.py --host 0.0.0.0 --port 8080

# Listen only on localhost
python src/streaming_server.py --host 127.0.0.1 --port 5000
```

### Multiple Camera Setup
Run multiple instances on different ports:
```bash
# Camera 1 on port 5001
python src/streaming_server.py --source 0 --port 5001

# Camera 2 on port 5002  
python src/streaming_server.py --source 1 --port 5002
```

### External Access (Internet)

⚠️ **Security Warning**: Only do this if you understand the security implications.

1. **Router Configuration:**
   - Forward port 5000 to your server's local IP
   - Access via: `http://YOUR_PUBLIC_IP:5000`

2. **Secure Options:**
   - Use VPN to access your local network
   - Set up reverse proxy with SSL (nginx, Apache)
   - Use cloud tunneling services (ngrok, cloudflare tunnel)

## 🚨 Alert Configuration

### Configure Webhooks
Edit `config/alerts.json`:
```json
{
  "webhooks": {
    "enabled": true,
    "urls": [
      "https://hooks.slack.com/your-webhook-url",
      "https://discord.com/api/webhooks/your-webhook"
    ]
  }
}
```

### SMS Integration
```json
{
  "sms": {
    "enabled": true,
    "api_key": "your-twilio-api-key",
    "phone_numbers": ["+1234567890", "+0987654321"]
  }
}
```

## 📊 API Endpoints

The system provides REST API endpoints:

- `GET /` - Web dashboard
- `GET /video_feed` - Live video stream
- `GET /api/status` - System status JSON
- `GET /api/detections` - Current detections JSON

### Example API Usage
```python
import requests

# Get system status
response = requests.get('http://server_ip:5000/api/status')
status = response.json()
print(f"Detections: {status['detections']}")
```

## 🔍 Troubleshooting

### Camera Issues
```bash
# List available cameras (Windows)
python -c "import cv2; [print(f'Camera {i}: {cv2.VideoCapture(i).isOpened()}') for i in range(5)]"

# Test specific camera
python test_webcam.py --camera 0
```

### Network Issues
- Check firewall settings (allow port 5000)
- Verify devices are on same network
- Try different ports if 5000 is blocked

### Performance Issues
- Lower video resolution in streaming_server.py
- Reduce frame rate
- Use CPU vs GPU based on hardware

## 🎯 Quick Commands Summary

**Start remote streaming:**
```bash
python src/streaming_server.py --source 0
```

**Access dashboard:**
```
http://YOUR_IP:5000
```

**Test webcam locally:**
```bash
python src/run_inference.py --source 0 --show
```

**Run tests:**
```bash
python -m pytest tests/ -v
```

This setup allows you to monitor the pool from anywhere on your network, receive real-time alerts, and view the detection results on any device with a web browser!

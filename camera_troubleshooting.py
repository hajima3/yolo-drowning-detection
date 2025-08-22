"""
WINDOWS CAMERA TROUBLESHOOTING GUIDE
====================================

❌ PROBLEM IDENTIFIED:
- Error -1072875772 = Camera access denied or driver issue
- DirectShow: "can't be used to capture by index"
- Media Foundation: Permission/driver problems

🔧 SOLUTIONS (Try in order):

1. CLOSE ALL CAMERA APPS
   - Close: Teams, Zoom, Skype, Chrome, Edge, OBS, etc.
   - Check Task Manager for hidden camera processes

2. WINDOWS CAMERA PERMISSIONS
   - Windows Settings > Privacy & Security > Camera
   - Turn ON "Camera access"
   - Turn ON "Let apps access your camera"  
   - Turn ON "Let desktop apps access your camera" ⭐ CRITICAL

3. CAMERA DRIVER UPDATE
   - Device Manager > Cameras (or Imaging devices)
   - Right-click your camera > Update driver
   - Choose "Search automatically"

4. RESTART REQUIRED
   - Restart your computer after permission changes

5. ALTERNATIVE: USE PHONE CAMERA
   - Install DroidCam or EpocCam
   - Use phone as webcam via USB/WiFi

6. TEST WITH CAMERA APP
   - Open Windows Camera app first
   - If it works, our code should work too

🚀 AFTER FIXING, RUN:
   python camera_solution.py

📱 IF STILL BROKEN - PHONE CAMERA SOLUTION:
   1. Install DroidCam: https://droidcam.app/
   2. Connect phone via USB
   3. Phone becomes Camera 1 or 2
"""

# Quick camera test after fixes
import cv2

def quick_test():
    print("🔍 QUICK CAMERA TEST AFTER FIXES...")
    
    for i in range(3):
        print(f"Testing camera {i}...")
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Camera {i} WORKING!")
                cap.release()
                return i
            cap.release()
    
    print("❌ Still not working - follow troubleshooting steps above")
    return None

if __name__ == "__main__":
    print(__doc__)
    quick_test()

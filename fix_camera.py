"""
Windows Camera Fix for YOLO Person Detection
Addresses MSMF error -1072875772
"""
import cv2
import numpy as np

def fix_windows_camera():
    """Fix Windows camera access issues."""
    print("🔧 WINDOWS CAMERA FIX")
    print("=" * 30)
    
    # Try different camera backends
    backends = [
        (cv2.CAP_DSHOW, "DirectShow"),
        (cv2.CAP_MSMF, "Media Foundation"),
        (cv2.CAP_ANY, "Auto")
    ]
    
    working_config = None
    
    for backend_id, backend_name in backends:
        print(f"\n🔍 Testing {backend_name} backend...")
        
        for camera_id in range(3):
            try:
                cap = cv2.VideoCapture(camera_id, backend_id)
                
                if cap.isOpened():
                    # Configure camera
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    cap.set(cv2.CAP_PROP_FPS, 30)
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer
                    
                    # Test frame capture
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        print(f"✅ Camera {camera_id} working with {backend_name}")
                        working_config = (camera_id, backend_id, backend_name)
                        cap.release()
                        return working_config
                    
                cap.release()
                
            except Exception as e:
                print(f"❌ Camera {camera_id} failed: {e}")
        
    print("❌ No working camera configuration found")
    return None

def test_yolo_simple():
    """Simple YOLO test with minimal confidence."""
    try:
        from ultralytics import YOLO
        
        print("\n🤖 Loading YOLO model...")
        model = YOLO('yolov8n.pt')
        
        # Test with dummy image
        dummy_img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        results = model.predict(dummy_img, conf=0.1, verbose=False)
        
        print("✅ YOLO model working!")
        return model
        
    except Exception as e:
        print(f"❌ YOLO error: {e}")
        return None

def run_fixed_detection():
    """Run person detection with fixed camera settings."""
    print("\n🎯 FIXED PERSON DETECTION")
    print("=" * 30)
    
    # Get working camera config
    config = fix_windows_camera()
    if not config:
        print("\n❌ CAMERA TROUBLESHOOTING NEEDED:")
        print("1. Close ALL apps using camera (Teams, Zoom, Chrome, etc.)")
        print("2. Windows Settings > Privacy > Camera > Allow apps to access camera")
        print("3. Device Manager > Cameras > Update driver")
        print("4. Restart computer")
        return
    
    camera_id, backend_id, backend_name = config
    print(f"\n✅ Using Camera {camera_id} with {backend_name}")
    
    # Test YOLO
    model = test_yolo_simple()
    if not model:
        return
    
    # Open camera with working config
    cap = cv2.VideoCapture(camera_id, backend_id)
    
    # Optimized settings for Windows
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 15)  # Lower FPS for stability
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    
    print("\n📹 Camera ready! Detection starting...")
    print("💡 Tips for detection:")
    print("   • Stand 4-8 feet from camera")
    print("   • Full body should be visible")
    print("   • Good lighting helps")
    print("   • Press 'q' to quit")
    
    frame_count = 0
    detection_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("⚠️ Frame read failed")
            continue
            
        frame_count += 1
        
        # Mirror effect
        frame = cv2.flip(frame, 1)
        
        # Detect every 3rd frame for performance
        if frame_count % 3 == 0:
            try:
                # Very low confidence for maximum detection
                results = model.predict(frame, conf=0.15, verbose=False)
                
                person_found = False
                
                for result in results:
                    if result.boxes is not None:
                        for box in result.boxes.data:
                            x1, y1, x2, y2, conf, cls = box.cpu().numpy()
                            
                            # Person class is 0
                            if int(cls) == 0:
                                person_found = True
                                detection_count += 1
                                
                                # Draw thick green box
                                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
                                
                                # Confidence text
                                conf_text = f"PERSON: {conf:.2f}"
                                cv2.putText(frame, conf_text, (int(x1), int(y1)-10), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                                
                                # Success indicator
                                cv2.putText(frame, "✅ DETECTED!", (10, 100), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
                
                # Status display
                if person_found:
                    status = f"✅ PERSON DETECTED! (Total: {detection_count})"
                    color = (0, 255, 0)
                else:
                    status = "❌ NO PERSON - Try moving or improving lighting"
                    color = (0, 0, 255)
                    
            except Exception as e:
                status = f"Error: {str(e)[:40]}"
                color = (0, 0, 255)
        
        # Display status
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.putText(frame, f"Frame: {frame_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show frame
        cv2.imshow('Fixed Person Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Frames: {frame_count}")
    print(f"   Detections: {detection_count}")
    
    if detection_count > 0:
        print("🎉 SUCCESS! Person detection is working!")
    else:
        print("❌ Still no detections. Check lighting and distance.")

if __name__ == "__main__":
    run_fixed_detection()

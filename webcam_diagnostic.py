"""
Webcam diagnostic tool to fix person detection issues.
"""
import cv2
import numpy as np

def diagnose_webcam():
    """Comprehensive webcam diagnosis."""
    print("🔍 WEBCAM DIAGNOSTIC TOOL")
    print("=" * 40)
    
    # Test multiple camera indices
    working_cameras = []
    for i in range(5):
        print(f"Testing camera index {i}...")
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                working_cameras.append(i)
                print(f"✅ Camera {i}: Working ({frame.shape})")
            else:
                print(f"❌ Camera {i}: Can't read frame")
            cap.release()
        else:
            print(f"❌ Camera {i}: Can't open")
    
    if not working_cameras:
        print("\n❌ NO WORKING CAMERAS FOUND!")
        print("🔧 Troubleshooting steps:")
        print("   1. Close all apps using camera (Teams, Skype, etc.)")
        print("   2. Check Windows camera privacy settings")
        print("   3. Restart the computer")
        print("   4. Update camera drivers")
        return None
    
    print(f"\n✅ Working cameras found: {working_cameras}")
    return working_cameras[0]

def test_yolo_detection():
    """Test YOLO with a sample image first."""
    print("\n🤖 Testing YOLO on sample image...")
    
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')
        
        # Create a test image with a person-like shape
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        test_img[100:400, 250:390] = [100, 100, 100]  # Gray rectangle (person-like)
        
        results = model.predict(test_img, conf=0.1, verbose=True)
        print(f"✅ YOLO working - detected {len(results[0].boxes) if results[0].boxes else 0} objects")
        return model
        
    except Exception as e:
        print(f"❌ YOLO error: {e}")
        return None

def test_camera_with_yolo(camera_index=0):
    """Test specific camera with YOLO detection."""
    print(f"\n📹 Testing Camera {camera_index} with YOLO...")
    
    # Load YOLO
    model = test_yolo_detection()
    if not model:
        return
    
    # Open camera with different backends
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
    cap = None
    
    for backend in backends:
        print(f"Trying backend: {backend}")
        cap = cv2.VideoCapture(camera_index, backend)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Success with backend {backend}")
                break
            cap.release()
        cap = None
    
    if not cap:
        print("❌ All backends failed")
        return
    
    # Set camera properties for better detection
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("✅ Camera opened successfully!")
    print("📋 Instructions:")
    print("   • Stand 3-6 feet from camera")
    print("   • Ensure good lighting")
    print("   • Try moving if not detected")
    print("   • Press 'q' to quit")
    
    frame_count = 0
    detection_count = 0
    last_detection_frame = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Can't read frame")
            break
            
        frame_count += 1
        
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Run YOLO every 5 frames for performance
        if frame_count % 5 == 0:
            try:
                # Lower confidence threshold for better detection
                results = model.predict(frame, conf=0.2, verbose=False)
                
                persons_detected = 0
                for result in results:
                    if result.boxes is not None:
                        for box in result.boxes.data:
                            x1, y1, x2, y2, conf, cls = box
                            
                            # Check if it's a person (class 0)
                            if int(cls) == 0:
                                persons_detected += 1
                                detection_count += 1
                                last_detection_frame = frame_count
                                
                                # Draw bright, thick bounding box
                                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                                
                                # Draw confidence score
                                conf_text = f"Person: {conf:.2f}"
                                cv2.putText(frame, conf_text, (int(x1), int(y1)-10), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                                
                                # Draw detection number
                                det_text = f"Detection #{detection_count}"
                                cv2.putText(frame, det_text, (int(x1), int(y2)+25), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Show detection status
                if persons_detected > 0:
                    status = f"✅ PERSON DETECTED! ({persons_detected})"
                    color = (0, 255, 0)
                else:
                    frames_since_detection = frame_count - last_detection_frame
                    status = f"❌ NO PERSON DETECTED (last: {frames_since_detection} frames ago)"
                    color = (0, 0, 255)
                    
            except Exception as e:
                status = f"Error: {str(e)[:50]}"
                color = (0, 0, 255)
        else:
            # Keep last status
            if 'status' not in locals():
                status = "Starting detection..."
                color = (255, 255, 255)
        
        # Draw status overlay
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Draw frame info
        info = f"Frame: {frame_count} | Total Detections: {detection_count}"
        cv2.putText(frame, info, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Draw tips
        if detection_count == 0 and frame_count > 100:
            tips = [
                "💡 Tips for better detection:",
                "  • Step back from camera",
                "  • Improve lighting",
                "  • Stand in center of frame",
                "  • Ensure full body visible"
            ]
            for i, tip in enumerate(tips):
                cv2.putText(frame, tip, (10, 100 + i*20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
        
        cv2.imshow('Person Detection Diagnostic', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 Detection Results:")
    print(f"   Frames processed: {frame_count}")
    print(f"   Person detections: {detection_count}")
    print(f"   Detection rate: {(detection_count/frame_count)*100:.1f}%")
    
    if detection_count > 0:
        print("✅ Person detection is working!")
    else:
        print("❌ No person detections - need troubleshooting")

def main():
    """Main diagnostic function."""
    print("🔍 YOLO PERSON DETECTION DIAGNOSTIC")
    print("=" * 50)
    
    # Step 1: Find working cameras
    camera_index = diagnose_webcam()
    if camera_index is None:
        return
    
    # Step 2: Test YOLO
    input(f"\n📹 Camera {camera_index} found. Press ENTER to test YOLO detection...")
    
    # Step 3: Test detection
    test_camera_with_yolo(camera_index)
    
    print("\n🎉 Diagnostic complete!")

if __name__ == "__main__":
    main()

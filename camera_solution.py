"""
Windows Camera Access Solution
Tries multiple methods to access camera
"""
import cv2
import numpy as np

def find_working_camera():
    """Find any working camera configuration."""
    print("🔍 SEARCHING FOR WORKING CAMERA...")
    
    # Try different methods
    methods = [
        (cv2.CAP_ANY, "Auto"),
        (cv2.CAP_DSHOW, "DirectShow"),
        (cv2.CAP_MSMF, "Media Foundation"),
        (cv2.CAP_V4L2, "Video4Linux"),
        (cv2.CAP_GSTREAMER, "GStreamer")
    ]
    
    for camera_idx in range(5):
        for backend, name in methods:
            try:
                print(f"Trying Camera {camera_idx} with {name}...")
                cap = cv2.VideoCapture(camera_idx, backend)
                
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        print(f"✅ SUCCESS! Camera {camera_idx} with {name}")
                        print(f"Frame size: {frame.shape}")
                        
                        # Test if we can actually use it
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                        
                        ret2, frame2 = cap.read()
                        if ret2:
                            cap.release()
                            return camera_idx, backend, name
                        
                cap.release()
                
            except Exception as e:
                print(f"❌ Failed: {e}")
    
    print("❌ No working camera found!")
    return None

def test_yolo_on_image():
    """Test YOLO on a static image first."""
    try:
        from ultralytics import YOLO
        
        print("\n🤖 Testing YOLO on static image...")
        model = YOLO('yolov8n.pt')
        
        # Create a simple test image
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        test_img[150:350, 220:420] = [128, 128, 128]  # Gray rectangle
        
        results = model.predict(test_img, conf=0.1, verbose=False)
        print(f"YOLO test complete - detected {len(results)} result sets")
        
        return model
        
    except Exception as e:
        print(f"❌ YOLO error: {e}")
        return None

def run_person_detection():
    """Run person detection with working camera."""
    # Find working camera
    result = find_working_camera()
    if not result:
        print("\n❌ CAMERA PROBLEM SOLUTIONS:")
        print("1. Make sure no other apps are using the camera")
        print("2. Windows Settings > Privacy & Security > Camera")
        print("3. Allow desktop apps to access camera")
        print("4. Try disconnecting and reconnecting USB camera")
        print("5. Restart computer")
        return
    
    camera_idx, backend, backend_name = result
    print(f"\n✅ Using Camera {camera_idx} with {backend_name}")
    
    # Test YOLO
    model = test_yolo_on_image()
    if not model:
        return
    
    # Open camera
    cap = cv2.VideoCapture(camera_idx, backend)
    
    # Configure camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    print("\n🎯 PERSON DETECTION STARTING...")
    print("Stand in front of camera and look for GREEN BOX around you")
    print("Press 'q' to quit")
    
    frame_count = 0
    person_detections = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame read failed")
            break
            
        frame_count += 1
        
        # Flip horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Run detection every few frames
        if frame_count % 3 == 0:  # Every 3rd frame
            try:
                # Use low confidence threshold
                results = model.predict(frame, conf=0.1, verbose=False)
                
                persons_found = 0
                
                for result in results:
                    if result.boxes is not None:
                        for box in result.boxes.data:
                            x1, y1, x2, y2, conf, cls = box.cpu().numpy()
                            
                            # Class 0 is person
                            if int(cls) == 0:
                                persons_found += 1
                                person_detections += 1
                                
                                # Draw GREEN box
                                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
                                
                                # Show confidence
                                text = f"Person: {conf:.2f}"
                                cv2.putText(frame, text, (int(x1), int(y1)-10), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Status
                if persons_found > 0:
                    status = f"✅ {persons_found} PERSON(S) DETECTED!"
                    color = (0, 255, 0)
                else:
                    status = "❌ No person detected"
                    color = (0, 0, 255)
                    
            except Exception as e:
                status = f"Detection error: {str(e)[:30]}"
                color = (255, 0, 0)
        
        # Draw status
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, f"Frame: {frame_count} | Detections: {person_detections}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Show instructions
        cv2.putText(frame, "Stand 3-6 feet away, full body visible", 
                   (10, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.putText(frame, "Press 'q' to quit", 
                   (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        cv2.imshow('Person Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 RESULTS:")
    print(f"Total frames: {frame_count}")
    print(f"Person detections: {person_detections}")
    print(f"Detection rate: {(person_detections/max(frame_count,1))*100:.1f}%")
    
    if person_detections > 0:
        print("🎉 SUCCESS! Person detection working!")
    else:
        print("❌ No detections. Try better lighting or different position.")

if __name__ == "__main__":
    run_person_detection()

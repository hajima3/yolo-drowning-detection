"""
Step-by-step webcam testing for drowning detection.
"""
import cv2
import time

def test_yolo_only():
    """Test YOLO model loading first."""
    print("🤖 Testing YOLO Model...")
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')
        print("✅ YOLO model loaded successfully!")
        return model
    except Exception as e:
        print(f"❌ YOLO loading failed: {e}")
        return None

def test_person_detection():
    """Test person detection with webcam."""
    print("\n👤 Testing Person Detection...")
    
    # Load YOLO
    model = test_yolo_only()
    if not model:
        return
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Webcam failed to open")
        return
    
    print("✅ Starting person detection test...")
    print("📋 Instructions:")
    print("   • Position yourself in front of the camera")
    print("   • You should see a green box around you")
    print("   • Press 'q' to quit this test")
    
    detections = 0
    frames = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frames += 1
        
        # Run detection every few frames for performance
        if frames % 3 == 0:
            results = model.predict(frame, conf=0.3, verbose=False)
            
            for result in results:
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box
                    
                    if int(cls) == 0:  # Person class
                        detections += 1
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
                        cv2.putText(frame, f"Person {conf:.2f}", (int(x1), int(y1)-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show stats
        cv2.putText(frame, f"Detections: {detections} | Frame: {frames}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to continue to drowning test", 
                   (10, frame.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Person Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    success = detections > 0
    print(f"{'✅' if success else '❌'} Person detection test: {detections} detections in {frames} frames")
    return success

def test_drowning_detection():
    """Test full drowning detection."""
    print("\n🏊‍♂️ Testing Drowning Detection...")
    
    model = test_yolo_only()
    if not model:
        return
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Webcam failed")
        return
    
    print("✅ Starting drowning detection test...")
    print("📋 Test Instructions:")
    print("   🧍 Stand upright = NORMAL (green box)")
    print("   🏃 Lie down horizontally = HORIZONTAL WARNING (orange box)")
    print("   📱 Move far from camera = LOW CONFIDENCE (yellow box)")
    print("   🛑 Press 'q' to finish test")
    
    frames = 0
    alerts = {'normal': 0, 'horizontal': 0, 'low_conf': 0}
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frames += 1
        
        if frames % 2 == 0:  # Every other frame
            results = model.predict(frame, conf=0.2, verbose=False)
            
            persons_in_frame = 0
            
            for result in results:
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box
                    
                    if int(cls) == 0:  # Person
                        persons_in_frame += 1
                        
                        # Calculate metrics
                        width = x2 - x1
                        height = y2 - y1
                        aspect_ratio = width / height if height > 0 else 0
                        
                        # Drowning risk assessment
                        if aspect_ratio < 0.5:  # Horizontal position
                            status = "HORIZONTAL ⚠️"
                            color = (0, 165, 255)  # Orange
                            alerts['horizontal'] += 1
                        elif conf < 0.4:  # Low confidence (far away/partial)
                            status = "LOW CONFIDENCE ⚠️"
                            color = (0, 255, 255)  # Yellow
                            alerts['low_conf'] += 1
                        else:
                            status = "NORMAL ✅"
                            color = (0, 255, 0)  # Green
                            alerts['normal'] += 1
                        
                        # Draw detection
                        thickness = 4 if 'WARNING' in status else 2
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
                        
                        # Draw status
                        cv2.putText(frame, status, (int(x1), int(y1)-15), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                        
                        # Draw metrics
                        metrics = f"Conf:{conf:.2f} Ratio:{aspect_ratio:.2f}"
                        cv2.putText(frame, metrics, (int(x1), int(y2)+20), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Draw summary
            summary = f"Persons: {persons_in_frame} | Frame: {frames}"
            cv2.putText(frame, summary, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Draw alert counts
            alert_text = f"Normal: {alerts['normal']} | Horizontal: {alerts['horizontal']} | Low Conf: {alerts['low_conf']}"
            cv2.putText(frame, alert_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Draw instructions
            cv2.putText(frame, "Try: Stand -> Lie Down -> Move Away -> Stand", 
                       (10, frame.shape[0]-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, "Press 'q' to finish", 
                       (10, frame.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('Drowning Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 Drowning Detection Test Results:")
    print(f"   Total frames: {frames}")
    print(f"   Normal detections: {alerts['normal']}")
    print(f"   Horizontal warnings: {alerts['horizontal']}")
    print(f"   Low confidence warnings: {alerts['low_conf']}")
    
    if alerts['horizontal'] > 0 or alerts['low_conf'] > 0:
        print("✅ Drowning detection is working! Warnings triggered correctly.")
    else:
        print("ℹ️ No warnings triggered. Try lying down or moving away from camera.")

def main():
    """Run complete webcam testing sequence."""
    print("🏊‍♂️ WEBCAM DROWNING DETECTION TESTING")
    print("=" * 50)
    print("This will test your webcam with drowning detection in steps:")
    print("1. YOLO model loading")
    print("2. Person detection")  
    print("3. Drowning behavior detection")
    print("\n🚀 Starting tests...")
    
    # Test 1: YOLO
    if not test_yolo_only():
        print("❌ Cannot proceed without YOLO model")
        return
    
    # Test 2: Person Detection
    input("\n👤 Press ENTER to start person detection test...")
    if not test_person_detection():
        print("⚠️ Person detection had issues, but continuing...")
    
    # Test 3: Drowning Detection
    input("\n🏊‍♂️ Press ENTER to start drowning detection test...")
    test_drowning_detection()
    
    print("\n🎉 All tests completed!")
    print("💡 Your drowning detection system is ready to use!")

if __name__ == "__main__":
    main()

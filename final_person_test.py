"""
FINAL PERSON DETECTION TEST
After fixing camera permissions, run this for YOLO person detection
"""
import cv2
from ultralytics import YOLO

def test_person_detection():
    """Simple, reliable person detection test."""
    print("🎯 FINAL PERSON DETECTION TEST")
    print("=" * 40)
    
    # Load YOLO
    print("Loading YOLO model...")
    model = YOLO('yolov8n.pt')
    print("✅ YOLO loaded!")
    
    # Open camera (try index 0 first)
    print("Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Camera 0 failed, trying camera 1...")
        cap = cv2.VideoCapture(1)
        
    if not cap.isOpened():
        print("❌ No camera available!")
        print("🔧 Make sure you fixed camera permissions first!")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("✅ Camera opened!")
    print("\n📋 INSTRUCTIONS:")
    print("• Stand 4-6 feet from camera")
    print("• Make sure your FULL BODY is visible")
    print("• Good lighting helps detection")
    print("• Look for GREEN BOX around you")
    print("• Press 'q' to quit")
    print("\nStarting detection in 3 seconds...")
    
    import time
    time.sleep(3)
    
    detection_count = 0
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame read failed")
            break
            
        frame_count += 1
        
        # Mirror the image
        frame = cv2.flip(frame, 1)
        
        # Run YOLO detection
        results = model.predict(frame, conf=0.3, verbose=False)  # 30% confidence
        
        person_detected = False
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box.cpu().numpy()
                    
                    # Class 0 = person
                    if int(cls) == 0:
                        person_detected = True
                        detection_count += 1
                        
                        # Draw THICK GREEN rectangle
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                        
                        # Show confidence
                        conf_text = f"PERSON: {conf:.2f}"
                        cv2.putText(frame, conf_text, (int(x1), int(y1)-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        
                        # Success message
                        cv2.putText(frame, "✅ PERSON DETECTED!", (10, 50), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
        
        # Status message
        if person_detected:
            status = f"✅ DETECTING! Total: {detection_count}"
            color = (0, 255, 0)
        else:
            status = "❌ No person - adjust position/lighting"
            color = (0, 0, 255)
        
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Frame counter
        cv2.putText(frame, f"Frame: {frame_count}", (10, frame.shape[0]-20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show frame
        cv2.imshow('Person Detection - Final Test', frame)
        
        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"Frames processed: {frame_count}")
    print(f"Person detections: {detection_count}")
    
    if detection_count > 0:
        print("🎉 SUCCESS! Person detection is working!")
        print("🏊‍♂️ Your drowning detection system is ready!")
    else:
        print("❌ No person detected. Check:")
        print("   • Camera permissions")
        print("   • Lighting conditions")
        print("   • Distance from camera")
        print("   • Full body visibility")

if __name__ == "__main__":
    test_person_detection()

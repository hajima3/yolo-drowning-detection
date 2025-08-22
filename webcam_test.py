"""
Simple webcam drowning detection test using the basic system.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cv2
import time
import numpy as np

# Try to import our drowning detector
try:
    from src.drowning_detector_advanced import DrowningDetector
    advanced_available = True
    print("✅ Advanced drowning detector available")
except ImportError:
    try:
        from drowning_detector_advanced import DrowningDetector
        advanced_available = True
        print("✅ Advanced drowning detector loaded")
    except ImportError:
        print("⚠️ Advanced detector not available, creating basic detector")
        advanced_available = False


def simple_webcam_test():
    """Simple webcam test with person detection."""
    print("\n🏊‍♂️ WEBCAM DROWNING DETECTION TEST")
    print("=" * 50)
    print("📹 Instructions:")
    print("   • Position yourself in front of the camera")
    print("   • Try different positions (standing, lying down)")
    print("   • Move around to test motion detection")
    print("   • Press 'q' to quit")
    print("   • Press 'SPACE' to pause/resume")
    print("\n🚀 Starting in 3 seconds...")
    time.sleep(3)
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open webcam")
        return
    
    print("✅ Webcam opened successfully")
    
    # Try to load YOLO model
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')
        print("✅ YOLO model loaded")
    except Exception as e:
        print(f"❌ Could not load YOLO model: {e}")
        cap.release()
        return
    
    frame_count = 0
    detection_count = 0
    
    print("\n🎯 Detection starting...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Run YOLO detection
        try:
            results = model.predict(source=frame, imgsz=640, conf=0.3, verbose=False)
            
            # Process detections
            persons_detected = 0
            if results and hasattr(results[0], 'boxes') and results[0].boxes is not None:
                for det in results[0].boxes.data.tolist():
                    xmin, ymin, xmax, ymax, score, cls = det[:6]
                    
                    # Only process person detections (class 0)
                    if int(cls) == 0:
                        persons_detected += 1
                        detection_count += 1
                        
                        # Draw bounding box
                        cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                        
                        # Calculate some basic metrics
                        width = xmax - xmin
                        height = ymax - ymin
                        aspect_ratio = width / height if height > 0 else 0
                        
                        # Simple drowning indicators
                        status = "NORMAL"
                        color = (0, 255, 0)  # Green
                        
                        if aspect_ratio < 0.4:  # Very horizontal
                            status = "HORIZONTAL ⚠️"
                            color = (0, 165, 255)  # Orange
                        elif score < 0.5:  # Low confidence (possible submersion)
                            status = "LOW CONFIDENCE ⚠️"
                            color = (0, 255, 255)  # Yellow
                        
                        # Draw person info
                        info_text = f"Person {persons_detected}: {status}"
                        cv2.putText(frame, info_text, (int(xmin), max(int(ymin)-10, 20)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                        
                        # Draw confidence and aspect ratio
                        details = f"Conf: {score:.2f} | Ratio: {aspect_ratio:.2f}"
                        cv2.putText(frame, details, (int(xmin), int(ymax)+20), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            
            # Draw overall status
            overall_status = f"Frame: {frame_count} | Persons: {persons_detected} | Total Detections: {detection_count}"
            cv2.putText(frame, overall_status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Draw instructions
            instructions = "Press 'q' to quit | Press SPACE to pause"
            cv2.putText(frame, instructions, (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
        except Exception as e:
            cv2.putText(frame, f"Detection Error: {str(e)[:50]}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Show frame
        cv2.imshow('Drowning Detection Test - Webcam', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):  # Pause
            cv2.waitKey(0)
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 Test Summary:")
    print(f"   Total frames: {frame_count}")
    print(f"   Person detections: {detection_count}")
    print(f"   Average detections per frame: {detection_count/frame_count:.2f}")
    print("✅ Webcam test completed!")


def advanced_webcam_test():
    """Advanced webcam test with full drowning detection."""
    if not advanced_available:
        print("❌ Advanced detector not available, running simple test")
        simple_webcam_test()
        return
    
    print("\n🏊‍♂️ ADVANCED WEBCAM DROWNING DETECTION TEST")
    print("=" * 60)
    
    # Initialize detector
    detector = DrowningDetector(fps=25.0)
    detector.load_model("yolov8n.pt")
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open webcam")
        return
    
    print("✅ Advanced drowning detection system ready")
    print("📹 Testing with webcam - try different positions and movements")
    
    frame_count = 0
    drowning_alerts = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        try:
            # Run advanced detection
            detections, water_mask = detector.predict_frame(frame)
            result = detector.advanced_drowning_detection(detections, water_mask)
            
            # Draw results on frame
            frame = draw_simple_results(frame, result, frame_count, drowning_alerts)
            
            if result['drowning_detected']:
                drowning_alerts += 1
                print(f"🚨 DROWNING ALERT #{drowning_alerts} at frame {frame_count}")
            
        except Exception as e:
            cv2.putText(frame, f"Error: {str(e)[:40]}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        cv2.imshow('Advanced Drowning Detection - Webcam', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Advanced test completed - {drowning_alerts} alerts in {frame_count} frames")


def draw_simple_results(frame, result, frame_count, alerts):
    """Draw detection results on frame."""
    # Status
    status = "🚨 DROWNING!" if result['drowning_detected'] else "✅ SAFE"
    color = (0, 0, 255) if result['drowning_detected'] else (0, 255, 0)
    
    cv2.putText(frame, f"{status} | Risk: {result['risk_level'].upper()}", 
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    # Stats
    stats = f"Frame: {frame_count} | Persons: {len(result['person_analyses'])} | Alerts: {alerts}"
    cv2.putText(frame, stats, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Person bounding boxes
    for person in result['person_analyses']:
        detection = person['detection']
        bbox = detection['bbox']
        
        # Color based on risk
        colors = {'low': (0, 255, 0), 'medium': (0, 255, 255), 'high': (0, 165, 255), 'critical': (0, 0, 255)}
        color = colors.get(person['risk_level'], (255, 255, 255))
        
        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
        cv2.putText(frame, f"Risk: {person['risk_level']}", 
                   (int(bbox[0]), int(bbox[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    return frame


if __name__ == "__main__":
    print("🎯 Choose test mode:")
    print("1. Simple webcam test (basic person detection)")
    print("2. Advanced drowning detection test")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        advanced_webcam_test()
    else:
        simple_webcam_test()

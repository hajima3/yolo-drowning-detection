"""
Direct webcam test with YOLO person detection.
"""
import cv2
import time

def quick_webcam_test():
    print("🎥 Quick Webcam + YOLO Test")
    print("=" * 30)
    
    # Test webcam first
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Webcam not available")
        print("💡 Troubleshooting:")
        print("   - Close other apps using camera")
        print("   - Check camera permissions")
        print("   - Try index 1: cv2.VideoCapture(1)")
        return
    
    print("✅ Webcam opened")
    
    # Test YOLO
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')
        print("✅ YOLO loaded")
    except Exception as e:
        print(f"❌ YOLO error: {e}")
        cap.release()
        return
    
    print("\n🚀 Starting detection...")
    print("📋 Instructions:")
    print("   • Stand in front of camera")
    print("   • Try lying down (horizontal)")
    print("   • Move around for motion test")
    print("   • Press 'q' to quit")
    
    frame_count = 0
    person_detections = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Can't read frame")
            break
            
        frame_count += 1
        
        # YOLO detection every 5 frames (for performance)
        if frame_count % 5 == 0:
            try:
                results = model.predict(frame, verbose=False)
                
                if results and len(results) > 0:
                    for box in results[0].boxes.data:
                        x1, y1, x2, y2, conf, cls = box
                        
                        if int(cls) == 0 and conf > 0.3:  # Person class
                            person_detections += 1
                            
                            # Draw box
                            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                            
                            # Calculate aspect ratio
                            width = x2 - x1
                            height = y2 - y1
                            ratio = width / height if height > 0 else 0
                            
                            # Simple drowning check
                            if ratio < 0.4:
                                status = "HORIZONTAL ⚠️"
                                color = (0, 165, 255)
                            elif conf < 0.5:
                                status = "LOW CONFIDENCE ⚠️"  
                                color = (0, 255, 255)
                            else:
                                status = "NORMAL ✅"
                                color = (0, 255, 0)
                            
                            # Draw info
                            cv2.putText(frame, status, (int(x1), int(y1)-10), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                            cv2.putText(frame, f"Conf: {conf:.2f} Ratio: {ratio:.2f}", 
                                       (int(x1), int(y2)+20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                            
            except Exception as e:
                cv2.putText(frame, f"Error: {str(e)[:30]}", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Draw stats
        cv2.putText(frame, f"Frame: {frame_count} | Detections: {person_detections}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0]-20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show frame
        cv2.imshow('Webcam Drowning Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n📊 Test Results:")
    print(f"   Frames processed: {frame_count}")
    print(f"   Person detections: {person_detections}")
    print("✅ Test completed!")

if __name__ == "__main__":
    quick_webcam_test()

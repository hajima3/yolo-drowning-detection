"""
Simple webcam test to verify camera is working.
"""
import cv2

def test_webcam():
    print("🎥 Testing webcam connection...")
    
    # Try to open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open webcam (index 0)")
        print("💡 Try these troubleshooting steps:")
        print("   1. Make sure no other apps are using the camera")
        print("   2. Check camera permissions in Windows settings")
        print("   3. Try different camera index (1, 2, etc.)")
        return False
    
    print("✅ Webcam opened successfully!")
    
    # Test frame capture
    ret, frame = cap.read()
    if ret:
        print(f"✅ Frame captured successfully: {frame.shape}")
        print("📹 Press 'q' to quit the test")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            cv2.imshow('Webcam Test - Press Q to quit', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        print("❌ Could not capture frame from webcam")
        
    cap.release()
    cv2.destroyAllWindows()
    print("🎥 Webcam test completed")
    return ret

if __name__ == "__main__":
    test_webcam()

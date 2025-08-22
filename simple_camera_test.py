"""
Simple Camera Test - Find what works
"""
import cv2

print("🔍 SIMPLE CAMERA TEST")

# Test camera 0 with DirectShow (usually works best on Windows)
print("Testing camera 0 with DirectShow...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if cap.isOpened():
    print("✅ Camera opened!")
    
    # Set properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Try to read a frame
    ret, frame = cap.read()
    if ret:
        print("✅ Frame captured successfully!")
        print(f"Frame shape: {frame.shape}")
        
        # Show for 3 seconds
        cv2.imshow('Camera Test', frame)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        
    else:
        print("❌ Could not capture frame")
        
    cap.release()
else:
    print("❌ Could not open camera")

print("Test complete!")

"""
Test script to demonstrate the enhanced drowning detection logic.
"""
import numpy as np
from src.drowning_detector import DrowningDetector


def test_drowning_detection():
    """Test the drowning detection system with simulated data."""
    print("🧪 Testing Enhanced Drowning Detection Logic\n")
    
    # Initialize detector
    detector = DrowningDetector(fps=25.0)
    detector.load_model("yolov8n.pt")
    
    print("✅ Detector initialized successfully")
    print(f"📊 Configuration: {detector.drowning_config}\n")
    
    # Test 1: Normal swimming detection (safe scenario)
    print("🔹 Test 1: Normal Swimming Detection")
    normal_detections = [{
        'class_id': 0,  # person
        'name': 'person',
        'confidence': 0.8,
        'bbox': [100, 100, 150, 200],  # Normal standing person
        'timestamp': 1.0,
        'center': [125, 150],
        'width': 50,
        'height': 100,
        'area': 5000,
        'aspect_ratio': 0.5  # Normal vertical person
    }]
    
    result = detector.comprehensive_drowning_detection(normal_detections)
    print(f"   Result: {'🚨 DROWNING' if result['drowning_detected'] else '✅ SAFE'}")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Alerts: {result['alerts']}\n")
    
    # Test 2: Horizontal position (potential drowning)
    print("🔹 Test 2: Horizontal Body Position")
    horizontal_detections = [{
        'class_id': 0,
        'name': 'person',
        'confidence': 0.7,
        'bbox': [100, 140, 200, 160],  # Wide, shallow box (horizontal person)
        'timestamp': 2.0,
        'center': [150, 150],
        'width': 100,
        'height': 20,
        'area': 2000,
        'aspect_ratio': 5.0  # Very horizontal
    }]
    
    result = detector.comprehensive_drowning_detection(horizontal_detections)
    print(f"   Result: {'🚨 DROWNING' if result['drowning_detected'] else '✅ SAFE'}")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Alerts: {result['alerts']}\n")
    
    # Test 3: Simulate rapid sinking motion
    print("🔹 Test 3: Rapid Sinking Motion Simulation")
    
    # Add several frames of a person sinking rapidly
    sinking_positions = [
        [125, 100],  # Starting position
        [125, 120],  # Moving down
        [125, 145],  # Moving down more
        [125, 175],  # Rapid descent
        [125, 210],  # Still sinking
    ]
    
    for i, pos in enumerate(sinking_positions):
        sinking_detection = [{
            'class_id': 0,
            'name': 'person',
            'confidence': 0.6 - i*0.05,  # Decreasing confidence (partial submersion)
            'bbox': [pos[0]-25, pos[1]-50, pos[0]+25, pos[1]+50],
            'timestamp': 3.0 + i*0.04,  # 25 FPS
            'center': pos,
            'width': 50,
            'height': 100,
            'area': 5000,
            'aspect_ratio': 0.5
        }]
        
        result = detector.comprehensive_drowning_detection(sinking_detection)
        print(f"   Frame {i+1}: Risk={result['risk_level']}, Conf={result['confidence']:.2f}")
        
        if result['drowning_detected']:
            print(f"   🚨 DROWNING DETECTED at frame {i+1}!")
            break
    
    print(f"   Final Alerts: {result['alerts']}\n")
    
    # Test 4: Low confidence detection (partial occlusion)
    print("🔹 Test 4: Partial Occlusion/Submersion")
    low_conf_detections = [{
        'class_id': 0,
        'name': 'person',
        'confidence': 0.3,  # Very low confidence
        'bbox': [100, 150, 130, 170],  # Small, partially visible
        'timestamp': 5.0,
        'center': [115, 160],
        'width': 30,
        'height': 20,
        'area': 600,
        'aspect_ratio': 1.5
    }]
    
    result = detector.comprehensive_drowning_detection(low_conf_detections)
    print(f"   Result: {'🚨 DROWNING' if result['drowning_detected'] else '✅ SAFE'}")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Alerts: {result['alerts']}\n")
    
    print("🎯 Testing Complete!")
    print("\n📋 Summary of Detection Capabilities:")
    print("   ✅ Movement tracking and velocity analysis")
    print("   ✅ Body position assessment (horizontal vs vertical)")
    print("   ✅ Temporal analysis with configurable thresholds")
    print("   ✅ Multi-factor risk scoring system")
    print("   ✅ Confidence-based alerting")
    print("   ✅ Real-time immobility detection")


if __name__ == "__main__":
    test_drowning_detection()

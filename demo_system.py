"""
Quick demo of the enhanced drowning detection system.
"""
from src.drowning_detector import DrowningDetector

# Initialize the detector
detector = DrowningDetector(fps=25.0)

print("🏊‍♂️ Enhanced YOLO Drowning Detection System")
print("=" * 50)
print("\n🎯 Key Features Implemented:")
print("✅ Multi-factor risk assessment")
print("✅ Temporal movement tracking")
print("✅ Body position analysis")
print("✅ Configurable alert thresholds")
print("✅ Real-time confidence scoring")

print(f"\n⚙️ Current Configuration:")
for key, value in detector.drowning_config.items():
    print(f"   {key}: {value}")

print(f"\n📊 Detection Algorithms:")
print("   1. Movement Velocity Analysis")
print("      - Tracks vertical/horizontal movement")
print("      - Detects rapid sinking motion")
print("      - Identifies struggling patterns")

print("   2. Body Position Assessment")
print("      - Horizontal vs vertical orientation")
print("      - Partial submersion detection")
print("      - Aspect ratio analysis")

print("   3. Temporal Behavior Analysis")
print("      - Immobility duration tracking")
print("      - Historical movement patterns")
print("      - Multi-frame correlation")

print("   4. Risk Scoring System")
print("      - Combines multiple indicators")
print("      - Confidence-based alerting")
print("      - Escalating risk levels")

print(f"\n🚀 Usage Examples:")
print("   # Test with webcam:")
print("   python src/run_inference.py --source 0 --show --detailed")
print("")
print("   # Analyze pool video:")
print("   python src/run_inference.py --source pool_video.mp4 --show --save output.mp4")
print("")
print("   # Background monitoring:")
print("   python src/run_inference.py --source rtsp://camera_url --alert-sound")

print(f"\n✨ The system is ready for testing!")

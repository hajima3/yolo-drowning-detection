"""
Advanced CLI to run drowning detection on video file or camera stream with comprehensive analysis.
"""
import argparse
import time
import cv2
import numpy as np

from src.drowning_detector import DrowningDetector


def draw_detection_info(frame, detection_result, show_detailed=True):
    """Draw detection information on the frame."""
    height, width = frame.shape[:2]
    
    # Draw overall status
    status_color = (0, 255, 0)  # Green = safe
    status_text = f"Status: SAFE (Risk: {detection_result['risk_level'].upper()})"
    
    if detection_result['drowning_detected']:
        status_color = (0, 0, 255)  # Red = danger
        status_text = f"⚠️ DROWNING DETECTED! (Confidence: {detection_result['confidence']:.2f})"
    elif detection_result['risk_level'] in ['high', 'medium']:
        status_color = (0, 165, 255)  # Orange = warning
        status_text = f"⚠️ WARNING: {detection_result['risk_level'].upper()} RISK"
    
    cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
    
    # Draw person analyses
    y_offset = 60
    for i, person in enumerate(detection_result['person_analyses']):
        detection = person['detection']
        xmin, ymin, xmax, ymax = map(int, detection['bbox'])
        
        # Color code based on risk level
        risk_colors = {
            'low': (0, 255, 0),      # Green
            'medium': (0, 255, 255),  # Yellow
            'high': (0, 165, 255),    # Orange
            'critical': (0, 0, 255)   # Red
        }
        color = risk_colors.get(person['risk_level'], (255, 255, 255))
        
        # Draw bounding box
        thickness = 3 if person['risk_level'] in ['high', 'critical'] else 2
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, thickness)
        
        # Draw person info
        person_text = f"Person {i+1}: {person['risk_level'].upper()} ({person['risk_score']:.2f})"
        cv2.putText(frame, person_text, (xmin, max(ymin-10, 15)), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        if show_detailed:
            # Show movement info
            movement = person['movement']
            if movement['is_sinking']:
                cv2.putText(frame, "SINKING!", (xmin, ymax + 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            if movement['is_struggling']:
                cv2.putText(frame, "STRUGGLING", (xmin, ymax + 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
            if movement['is_immobile']:
                cv2.putText(frame, "IMMOBILE", (xmin, ymax + 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Show alerts on the side
        for j, alert in enumerate(person['alerts'][:3]):  # Show max 3 alerts
            cv2.putText(frame, f"• {alert}", (10, y_offset + j * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        y_offset += len(person['alerts'][:3]) * 20 + 10
    
    return frame


def main():
    parser = argparse.ArgumentParser(description="Advanced YOLO Drowning Detection System")
    parser.add_argument('--source', '-s', default=0, 
                       help='Path to video file, camera index, or RTSP URL')
    parser.add_argument('--model', '-m', default='yolov8n.pt', 
                       help='YOLO model path or ultralytics short name')
    parser.add_argument('--show', action='store_true', 
                       help='Show video with detections and analysis')
    parser.add_argument('--fps', type=float, default=None,
                       help='Override FPS for temporal analysis (auto-detect if not provided)')
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed movement analysis on video')
    parser.add_argument('--save', type=str, default=None,
                       help='Save output video to specified path')
    parser.add_argument('--alert-sound', action='store_true',
                       help='Play sound alert when drowning is detected')
    
    args = parser.parse_args()

    # Initialize detector with FPS
    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print(f'❌ Failed to open source: {args.source}')
        return

    detected_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    actual_fps = args.fps if args.fps else detected_fps
    
    print(f"📹 Source opened successfully")
    print(f"🎬 FPS: {actual_fps} (detected: {detected_fps})")
    
    det = DrowningDetector(fps=actual_fps)
    det.load_model(args.model)
    print(f"🤖 YOLO model loaded: {args.model}")
    print(f"🏊‍♂️ Drowning detection system initialized")
    print("\n🚀 Starting detection... Press 'q' to quit\n")

    # Video writer setup if saving
    video_writer = None
    if args.save:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(args.save, fourcc, actual_fps, (frame_width, frame_height))

    frame_count = 0
    total_processing_time = 0
    drowning_alerts = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            t0 = time.time()
            
            # Run YOLO detection
            detections = det.predict_frame(frame)
            
            # Run comprehensive drowning detection
            drowning_result = det.comprehensive_drowning_detection(detections)
            
            t1 = time.time()
            processing_time = (t1 - t0) * 1000
            total_processing_time += processing_time
            
            # Alert handling
            if drowning_result['drowning_detected']:
                drowning_alerts += 1
                print(f"🚨 FRAME {frame_count}: DROWNING DETECTED! Confidence: {drowning_result['confidence']:.2f}")
                for alert in drowning_result['alerts']:
                    print(f"   • {alert}")
                
                if args.alert_sound:
                    # You could add sound alert here (e.g., using playsound library)
                    print("🔊 ALERT SOUND!")
            
            # Display processing
            if args.show:
                display_frame = draw_detection_info(frame, drowning_result, args.detailed)
                
                # Add performance info
                cv2.putText(display_frame, f"FPS: {1000/processing_time:.1f} | Frame: {frame_count}", 
                           (10, display_frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                cv2.imshow('Drowning Detection System', display_frame)
                
                if video_writer:
                    video_writer.write(display_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord(' '):  # Spacebar to pause
                    cv2.waitKey(0)
            else:
                # Console output mode
                if frame_count % 30 == 0:  # Print every 30 frames
                    avg_fps = 1000 / (total_processing_time / frame_count)
                    print(f"📊 Frame {frame_count}: {len(detections)} detections, "
                          f"Risk: {drowning_result['risk_level']}, "
                          f"Avg FPS: {avg_fps:.1f}, "
                          f"Total alerts: {drowning_alerts}")

    except KeyboardInterrupt:
        print("\n⏹️ Detection stopped by user")
    
    finally:
        # Cleanup
        cap.release()
        if video_writer:
            video_writer.release()
        cv2.destroyAllWindows()
        
        # Final statistics
        if frame_count > 0:
            avg_processing_time = total_processing_time / frame_count
            avg_fps = 1000 / avg_processing_time
            print(f"\n📈 DETECTION SUMMARY:")
            print(f"   Total frames processed: {frame_count}")
            print(f"   Average processing time: {avg_processing_time:.2f} ms/frame")
            print(f"   Average FPS: {avg_fps:.1f}")
            print(f"   Total drowning alerts: {drowning_alerts}")
            if args.save:
                print(f"   Video saved to: {args.save}")


if __name__ == '__main__':
    main()

"""
Enhanced run_inference.py to use the advanced drowning detection system.
"""
import argparse
import time
import cv2
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.drowning_detector_advanced import DrowningDetector


def draw_advanced_detection_info(frame, detection_result, show_detailed=True):
    """Draw comprehensive detection information on the frame."""
    height, width = frame.shape[:2]
    
    # Draw overall status with enhanced styling
    status_color = (0, 255, 0)  # Green = safe
    status_text = f"Status: SAFE (Risk: {detection_result['risk_level'].upper()})"
    
    if detection_result['drowning_detected']:
        status_color = (0, 0, 255)  # Red = danger
        status_text = f"🚨 DROWNING DETECTED! (Confidence: {detection_result['confidence']:.2f})"
    elif detection_result['risk_level'] in ['high', 'critical']:
        status_color = (0, 165, 255)  # Orange = warning
        status_text = f"⚠️ {detection_result['risk_level'].upper()} RISK (Conf: {detection_result['confidence']:.2f})"
    elif detection_result['risk_level'] == 'medium':
        status_color = (0, 255, 255)  # Yellow = caution
        status_text = f"⚠️ MEDIUM RISK (Conf: {detection_result['confidence']:.2f})"
    
    # Draw status with background
    text_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
    cv2.rectangle(frame, (5, 5), (text_size[0] + 15, 35), (0, 0, 0), -1)
    cv2.putText(frame, status_text, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
    
    # Environmental context
    env_info = detection_result['environmental_context']
    env_text = f"Pool: {'✓' if env_info['water_detected'] else '✗'} | Persons: {env_info['total_persons']} | Tracks: {detection_result['tracking_info']['active_tracks']}"
    cv2.putText(frame, env_text, (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Draw person analyses
    y_offset = 80
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
        
        # Draw bounding box with thickness based on risk
        thickness = 4 if person['risk_level'] in ['high', 'critical'] else 2
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, thickness)
        
        # Draw track ID and risk info
        track_info = f"ID:{person['track_id']} | {person['risk_level'].upper()} ({person['risk_score']:.2f})"
        
        # Background for text
        text_size = cv2.getTextSize(track_info, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        cv2.rectangle(frame, (xmin, max(ymin-25, 0)), (xmin + text_size[0] + 10, max(ymin-5, 20)), (0, 0, 0), -1)
        cv2.putText(frame, track_info, (xmin + 5, max(ymin-10, 15)), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Show alerts for high-risk persons
        if person['risk_level'] in ['high', 'critical'] and show_detailed:
            for j, alert in enumerate(person['alerts'][:2]):  # Show max 2 alerts per person
                alert_text = f"• {alert}"
                cv2.putText(frame, alert_text, (10, y_offset + j * 18), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            y_offset += len(person['alerts'][:2]) * 18 + 5
    
    # General alerts
    if detection_result['alerts'] and y_offset < height - 50:
        cv2.putText(frame, "ALERTS:", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        y_offset += 20
        for alert in detection_result['alerts'][:3]:
            cv2.putText(frame, f"• {alert}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            y_offset += 18
    
    return frame


def main():
    parser = argparse.ArgumentParser(description="Advanced YOLO Drowning Detection System v2.0")
    parser.add_argument('--source', '-s', default=0, 
                       help='Path to video file, camera index, or RTSP URL')
    parser.add_argument('--model', '-m', default='yolov8n.pt', 
                       help='YOLO model path or ultralytics short name')
    parser.add_argument('--show', action='store_true', 
                       help='Show video with detections and analysis')
    parser.add_argument('--fps', type=float, default=None,
                       help='Override FPS for temporal analysis')
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed analysis information')
    parser.add_argument('--save', type=str, default=None,
                       help='Save output video to specified path')
    parser.add_argument('--pose', action='store_true',
                       help='Enable pose estimation for enhanced detection')
    parser.add_argument('--water-detection', action='store_true', default=True,
                       help='Enable automatic water area detection')
    
    args = parser.parse_args()

    # Initialize video capture
    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print(f'❌ Failed to open source: {args.source}')
        return

    detected_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    actual_fps = args.fps if args.fps else detected_fps
    
    print(f"🏊‍♂️ ADVANCED DROWNING DETECTION SYSTEM v2.0")
    print("=" * 50)
    print(f"📹 Source: {args.source}")
    print(f"🎬 FPS: {actual_fps} (detected: {detected_fps})")
    
    # Initialize advanced detector
    detector = DrowningDetector(fps=actual_fps)
    detector.load_model(args.model, enable_pose=args.pose)
    
    print(f"🤖 YOLO model: {args.model}")
    print(f"🧠 Advanced features enabled:")
    print(f"   • Multi-person tracking: ✓")
    print(f"   • Water area detection: {'✓' if args.water_detection else '✗'}")
    print(f"   • Pose estimation: {'✓' if args.pose else '✗'}")
    print(f"   • Temporal analysis: ✓")
    print(f"   • Environmental context: ✓")
    print("\n🚀 Starting detection... Press 'q' to quit, 'SPACE' to pause\n")

    # Video writer setup
    video_writer = None
    if args.save:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(args.save, fourcc, actual_fps, (frame_width, frame_height))

    frame_count = 0
    total_processing_time = 0
    drowning_alerts = 0
    risk_statistics = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            t0 = time.time()
            
            # Run advanced detection
            detections, water_mask = detector.predict_frame(frame)
            drowning_result = detector.advanced_drowning_detection(detections, water_mask)
            
            t1 = time.time()
            processing_time = (t1 - t0) * 1000
            total_processing_time += processing_time
            
            # Update statistics
            risk_statistics[drowning_result['risk_level']] += 1
            
            # Alert handling
            if drowning_result['drowning_detected']:
                drowning_alerts += 1
                print(f"🚨 FRAME {frame_count}: DROWNING DETECTED!")
                print(f"   Confidence: {drowning_result['confidence']:.2f}")
                print(f"   Persons at risk: {len([p for p in drowning_result['person_analyses'] if p['risk_level'] in ['high', 'critical']])}")
                for alert in drowning_result['alerts'][:3]:
                    print(f"   • {alert}")
                print()
            
            # Display processing
            if args.show:
                display_frame = draw_advanced_detection_info(frame, drowning_result, args.detailed)
                
                # Add performance info
                perf_text = f"FPS: {1000/processing_time:.1f} | Frame: {frame_count} | Alerts: {drowning_alerts}"
                cv2.putText(display_frame, perf_text, 
                           (10, display_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                
                # Show water mask if detected
                if water_mask is not None and args.detailed:
                    water_overlay = cv2.applyColorMap(water_mask, cv2.COLORMAP_OCEAN)
                    display_frame = cv2.addWeighted(display_frame, 0.8, water_overlay, 0.2, 0)
                
                cv2.imshow('Advanced Drowning Detection System', display_frame)
                
                if video_writer:
                    video_writer.write(display_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord(' '):  # Spacebar to pause
                    cv2.waitKey(0)
            else:
                # Console output mode
                if frame_count % 60 == 0:  # Print every 60 frames
                    avg_fps = 1000 / (total_processing_time / frame_count)
                    active_tracks = drowning_result['tracking_info']['active_tracks']
                    print(f"📊 Frame {frame_count}: "
                          f"Tracks: {active_tracks}, "
                          f"Risk: {drowning_result['risk_level']}, "
                          f"FPS: {avg_fps:.1f}, "
                          f"Alerts: {drowning_alerts}")

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
            
            print(f"\n📈 FINAL STATISTICS")
            print("=" * 50)
            print(f"📊 Processing Performance:")
            print(f"   Total frames: {frame_count}")
            print(f"   Average processing: {avg_processing_time:.2f} ms/frame")
            print(f"   Average FPS: {avg_fps:.1f}")
            
            print(f"\n🎯 Detection Results:")
            print(f"   Total drowning alerts: {drowning_alerts}")
            print(f"   Alert rate: {(drowning_alerts/frame_count)*100:.2f}%")
            
            print(f"\n📊 Risk Level Distribution:")
            total_risk_frames = sum(risk_statistics.values())
            for level, count in risk_statistics.items():
                percentage = (count / total_risk_frames) * 100 if total_risk_frames > 0 else 0
                print(f"   {level.upper():<8}: {count:>6} frames ({percentage:>5.1f}%)")
            
            if args.save:
                print(f"\n💾 Video saved to: {args.save}")


if __name__ == '__main__':
    main()

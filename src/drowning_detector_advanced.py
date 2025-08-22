"""
Advanced wrapper around Ultralytics YOLO for person detection with comprehensive
drowning detection algorithms including pose estimation and environmental analysis.
"""
from typing import Optional, List, Dict, Tuple, Union
import numpy as np
import time
import cv2
from collections import defaultdict, deque
import math


class PersonTracker:
    """Advanced person tracking for multi-person drowning detection."""
    
    def __init__(self, max_tracking_distance: float = 50.0, max_tracking_frames: int = 30):
        self.tracks = {}  # track_id -> track_data
        self.next_track_id = 1
        self.max_tracking_distance = max_tracking_distance
        self.max_tracking_frames = max_tracking_frames
        
    def update_tracks(self, detections: List[Dict]) -> Dict[int, Dict]:
        """Update person tracks with new detections."""
        current_time = time.time()
        
        # Remove old tracks
        tracks_to_remove = []
        for track_id, track_data in self.tracks.items():
            if current_time - track_data['last_seen'] > self.max_tracking_frames / 25.0:  # Assume 25 FPS
                tracks_to_remove.append(track_id)
        
        for track_id in tracks_to_remove:
            del self.tracks[track_id]
        
        # Match detections to existing tracks
        matched_tracks = set()
        unmatched_detections = []
        
        for detection in detections:
            if detection['class_id'] != 0:  # Only track persons
                continue
                
            best_track_id = None
            best_distance = float('inf')
            
            detection_center = np.array(detection['center'])
            
            for track_id, track_data in self.tracks.items():
                if track_id in matched_tracks:
                    continue
                    
                last_center = np.array(track_data['positions'][-1])
                distance = np.linalg.norm(detection_center - last_center)
                
                if distance < self.max_tracking_distance and distance < best_distance:
                    best_distance = distance
                    best_track_id = track_id
            
            if best_track_id is not None:
                # Update existing track
                track_data = self.tracks[best_track_id]
                track_data['positions'].append(detection['center'])
                track_data['detections'].append(detection)
                track_data['last_seen'] = current_time
                track_data['velocities'] = self._calculate_velocities(track_data['positions'])
                
                # Keep only recent data
                max_history = 50
                if len(track_data['positions']) > max_history:
                    track_data['positions'] = track_data['positions'][-max_history:]
                    track_data['detections'] = track_data['detections'][-max_history:]
                    
                matched_tracks.add(best_track_id)
            else:
                unmatched_detections.append(detection)
        
        # Create new tracks for unmatched detections
        for detection in unmatched_detections:
            track_id = self.next_track_id
            self.next_track_id += 1
            
            self.tracks[track_id] = {
                'positions': deque([detection['center']], maxlen=50),
                'detections': deque([detection], maxlen=50),
                'velocities': deque(maxlen=49),
                'last_seen': current_time,
                'created_at': current_time
            }
        
        return self.tracks
    
    def _calculate_velocities(self, positions: deque) -> deque:
        """Calculate velocities from position history."""
        velocities = deque(maxlen=len(positions)-1)
        for i in range(1, len(positions)):
            pos_diff = np.array(positions[i]) - np.array(positions[i-1])
            velocity = np.linalg.norm(pos_diff)
            velocities.append(velocity)
        return velocities


class WaterDetector:
    """Detect water areas in the frame for better context awareness."""
    
    def __init__(self):
        self.water_mask = None
        self.pool_boundaries = None
        
    def detect_water_areas(self, frame: np.ndarray) -> np.ndarray:
        """Detect water/pool areas in the frame using color and texture analysis."""
        # Convert to HSV for better water detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define water color ranges (blue/cyan tones)
        lower_blue1 = np.array([100, 50, 50])
        upper_blue1 = np.array([130, 255, 255])
        
        lower_blue2 = np.array([80, 30, 30])
        upper_blue2 = np.array([120, 200, 200])
        
        # Create masks for water detection
        mask1 = cv2.inRange(hsv, lower_blue1, upper_blue1)
        mask2 = cv2.inRange(hsv, lower_blue2, upper_blue2)
        water_mask = cv2.bitwise_or(mask1, mask2)
        
        # Apply morphological operations to clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_CLOSE, kernel)
        water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_OPEN, kernel)
        
        # Find the largest connected component (likely the pool)
        contours, _ = cv2.findContours(water_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 1000:  # Minimum pool size
                self.pool_boundaries = largest_contour
                water_mask = np.zeros_like(water_mask)
                cv2.fillPoly(water_mask, [largest_contour], 255)
        
        self.water_mask = water_mask
        return water_mask
    
    def is_in_water(self, center_point: Tuple[float, float]) -> bool:
        """Check if a point is within the detected water area."""
        if self.water_mask is None:
            return True  # Assume in water if no detection
            
        x, y = int(center_point[0]), int(center_point[1])
        if 0 <= x < self.water_mask.shape[1] and 0 <= y < self.water_mask.shape[0]:
            return self.water_mask[y, x] > 0
        return False


class DrowningDetector:
    def __init__(self, device: Optional[str] = None, fps: float = 25.0):
        """Create detector object. Model is not loaded until load_model() is called.

        Args:
            device: torch device string, e.g. 'cpu' or 'cuda:0'. If None, let ultralytics pick.
            fps: Expected frames per second of the video stream for temporal analysis.
        """
        self.model = None
        self.pose_model = None
        self.device = device
        self.fps = fps
        
        # Advanced tracking and detection components
        self.person_tracker = PersonTracker()
        self.water_detector = WaterDetector()
        
        # Detection history for temporal analysis
        self.detection_history = []
        self.max_history_frames = int(fps * 15)  # Keep 15 seconds of history
        
        # Enhanced drowning detection parameters
        self.drowning_config = {
            # Basic detection
            'min_detection_confidence': 0.4,
            'person_class_id': 0,
            
            # Movement thresholds
            'vertical_movement_threshold': 3.0,      # pixels per frame
            'horizontal_movement_threshold': 8.0,    # pixels per frame
            'rapid_sinking_threshold': 15.0,         # pixels per frame downward
            'struggling_motion_variance': 12.0,      # motion variance threshold
            
            # Temporal thresholds
            'immobile_time_threshold': 2.5,          # seconds
            'distress_time_threshold': 1.5,          # seconds for distress patterns
            'critical_time_threshold': 4.0,          # seconds for critical situations
            
            # Body position analysis
            'aspect_ratio_threshold': 0.35,          # width/height for horizontal detection
            'submersion_confidence_drop': 0.3,       # confidence drop indicating submersion
            'normal_person_ratio': 2.0,              # normal height/width ratio
            
            # Advanced features
            'water_detection_enabled': True,
            'pose_estimation_enabled': False,        # Will enable when pose model is loaded
            'multi_person_tracking': True,
            
            # Alert thresholds
            'medium_risk_threshold': 0.4,
            'high_risk_threshold': 0.6,
            'critical_risk_threshold': 0.8,
            
            # Environmental factors
            'pool_edge_safety_margin': 20,           # pixels from pool edge
            'minimum_person_size': 400,              # minimum bbox area for valid detection
        }

    def load_model(self, model_path: str = "yolov8n.pt", enable_pose: bool = False) -> None:
        """Load a YOLO model from a local path or one of the Ultralytics short names."""
        try:
            from ultralytics import YOLO
        except Exception as e:
            raise RuntimeError("ultralytics package is required. Install with pip install ultralytics") from e

        self.model = YOLO(model_path)
        if self.device:
            try:
                self.model.to(self.device)
            except Exception:
                pass
        
        # Load pose estimation model if requested
        if enable_pose:
            try:
                self.pose_model = YOLO('yolov8n-pose.pt')
                if self.device:
                    self.pose_model.to(self.device)
                self.drowning_config['pose_estimation_enabled'] = True
                print("✅ Pose estimation model loaded successfully")
            except Exception as e:
                print(f"⚠️ Could not load pose model: {e}")
                self.drowning_config['pose_estimation_enabled'] = False

    def predict_frame(self, frame) -> Tuple[List[Dict], Optional[np.ndarray]]:
        """Run inference on a single frame and return detections with environmental context."""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Detect water areas for context
        water_mask = None
        if self.drowning_config['water_detection_enabled']:
            water_mask = self.water_detector.detect_water_areas(frame)

        # Run YOLO detection
        results = self.model.predict(source=frame, imgsz=640, conf=0.25, verbose=False)

        if not results:
            return [], water_mask
            
        r = results[0]
        detections = []
        
        for det in r.boxes.data.tolist() if hasattr(r.boxes, 'data') else []:
            xmin, ymin, xmax, ymax, score, cls = det[:6]
            
            # Enhanced detection data
            detection = {
                "class_id": int(cls),
                "name": r.names[int(cls)] if hasattr(r, 'names') else str(int(cls)),
                "confidence": float(score),
                "bbox": [float(xmin), float(ymin), float(xmax), float(ymax)],
                "timestamp": time.time(),
                "center": [(xmin + xmax) / 2, (ymin + ymax) / 2],
                "width": xmax - xmin,
                "height": ymax - ymin,
                "area": (xmax - xmin) * (ymax - ymin),
                "aspect_ratio": (xmax - xmin) / (ymax - ymin) if (ymax - ymin) > 0 else 0,
                
                # Environmental context
                "in_water": self.water_detector.is_in_water([(xmin + xmax) / 2, (ymin + ymax) / 2]),
                "distance_to_pool_edge": self._calculate_pool_distance([(xmin + xmax) / 2, (ymin + ymax) / 2]),
                
                # Additional metrics
                "visibility_score": score,  # Simplified for now
            }
            
            detections.append(detection)
        
        return detections, water_mask
    
    def _calculate_pool_distance(self, center_point: Tuple[float, float]) -> float:
        """Calculate distance from person to pool edge."""
        if self.water_detector.pool_boundaries is None:
            return 0.0
            
        distance = cv2.pointPolygonTest(self.water_detector.pool_boundaries, 
                                      (center_point[0], center_point[1]), True)
        return abs(distance)

    def advanced_drowning_detection(self, current_detections: List[Dict], water_mask: np.ndarray = None) -> Dict:
        """State-of-the-art drowning detection using multiple AI techniques."""
        # Update tracking
        tracks = self.person_tracker.update_tracks(current_detections)
        
        result = {
            'drowning_detected': False,
            'confidence': 0.0,
            'risk_level': 'low',
            'alerts': [],
            'person_analyses': [],
            'environmental_context': {
                'water_detected': water_mask is not None,
                'pool_area': np.sum(water_mask > 0) if water_mask is not None else 0,
                'total_persons': len([d for d in current_detections if d['class_id'] == 0])
            },
            'tracking_info': {
                'active_tracks': len(tracks),
            }
        }
        
        if not tracks:
            return result
        
        # Analyze each tracked person
        for track_id, track_data in tracks.items():
            if len(track_data['detections']) == 0:
                continue
                
            current_detection = track_data['detections'][-1]
            if current_detection['class_id'] != 0:  # Only analyze persons
                continue
            
            person_analysis = self._analyze_person_comprehensive(track_data, track_id)
            result['person_analyses'].append(person_analysis)
            
            # Update overall result based on highest risk person
            if person_analysis['risk_score'] > result['confidence']:
                result['confidence'] = person_analysis['risk_score']
                result['risk_level'] = person_analysis['risk_level']
                result['alerts'] = person_analysis['alerts'].copy()
        
        # Determine final drowning detection
        result['drowning_detected'] = result['confidence'] >= self.drowning_config['critical_risk_threshold']
        
        return result
    
    def _analyze_person_comprehensive(self, track_data: Dict, track_id: int) -> Dict:
        """Comprehensive analysis of a single person's behavior."""
        current_detection = track_data['detections'][-1]
        
        analysis = {
            'track_id': track_id,
            'detection': current_detection,
            'risk_score': 0.0,
            'risk_level': 'low',
            'alerts': [],
        }
        
        # Calculate risk score based on multiple factors
        risk_score = 0.0
        
        # Movement analysis
        if len(track_data['positions']) > 3:
            positions = np.array(list(track_data['positions']))
            
            # Check for rapid vertical movement (sinking)
            if len(positions) >= 5:
                recent_positions = positions[-5:]
                vertical_trend = np.polyfit(range(len(recent_positions)), recent_positions[:, 1], 1)[0]
                
                if vertical_trend > self.drowning_config['rapid_sinking_threshold']:
                    risk_score += 0.4
                    analysis['alerts'].append("Rapid downward movement detected")
            
            # Check for movement variance (struggling)
            if len(track_data['velocities']) > 3:
                velocities = list(track_data['velocities'])
                velocity_std = np.std(velocities)
                if velocity_std > self.drowning_config['struggling_motion_variance']:
                    risk_score += 0.3
                    analysis['alerts'].append("Erratic movement patterns detected")
        
        # Position analysis
        aspect_ratio = current_detection['aspect_ratio']
        if aspect_ratio < self.drowning_config['aspect_ratio_threshold']:
            risk_score += 0.4
            analysis['alerts'].append("Horizontal body position detected")
        
        # Confidence drop analysis (submersion indicator)
        if len(track_data['detections']) > 3:
            recent_confidences = [d['confidence'] for d in list(track_data['detections'])[-3:]]
            confidence_trend = np.polyfit(range(len(recent_confidences)), recent_confidences, 1)[0]
            
            if confidence_trend < -self.drowning_config['submersion_confidence_drop']:
                risk_score += 0.3
                analysis['alerts'].append("Detection confidence decreasing (possible submersion)")
        
        # Environmental factors
        if not current_detection.get('in_water', True):
            risk_score = 0.0  # Not in water = no drowning risk
        
        analysis['risk_score'] = min(risk_score, 1.0)
        
        # Determine risk level
        if risk_score >= self.drowning_config['critical_risk_threshold']:
            analysis['risk_level'] = 'critical'
        elif risk_score >= self.drowning_config['high_risk_threshold']:
            analysis['risk_level'] = 'high'
        elif risk_score >= self.drowning_config['medium_risk_threshold']:
            analysis['risk_level'] = 'medium'
        
        return analysis

    # Legacy methods for backward compatibility
    def comprehensive_drowning_detection(self, current_detections: List[Dict]) -> Dict:
        """Legacy method - redirects to advanced detection system."""
        # Ensure detections have required fields
        for detection in current_detections:
            if 'timestamp' not in detection:
                detection['timestamp'] = time.time()
            if 'center' not in detection:
                bbox = detection['bbox']
                detection['center'] = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
            if 'area' not in detection:
                bbox = detection['bbox']
                detection['area'] = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            if 'aspect_ratio' not in detection:
                bbox = detection['bbox']
                width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                detection['aspect_ratio'] = width / height if height > 0 else 0
        
        return self.advanced_drowning_detection(current_detections)

    def simple_drowning_heuristic(self, history: List[Dict]) -> bool:
        """Legacy method - now redirects to comprehensive detection."""
        if not history:
            return False
        
        current_detections = history[-1].get('detections', []) if history else []
        result = self.advanced_drowning_detection(current_detections)
        return result['drowning_detected']

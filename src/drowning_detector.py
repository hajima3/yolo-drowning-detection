"""
Advanced wrapper around Ultralytics YOLO for person detection with comprehensive
drowning detection algorithms including pose estimation and environmental analysis.
"""
from typing import Optional, List, Dict, Tuple, Union
import numpy as np
import time
import cv2
from scipy import ndimage
from collections import defaultdict, deque
import math


class PersonTracker:
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
        }mport Optional, List, Dict, Tuple, Union
import numpy as np
import time
import cv2
from scipy import ndimage
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
                track_data['accelerations'] = self._calculate_accelerations(track_data['velocities'])
                
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
                'accelerations': deque(maxlen=48),
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
    
    def _calculate_accelerations(self, velocities: deque) -> deque:
        """Calculate accelerations from velocity history."""
        accelerations = deque(maxlen=len(velocities)-1)
        for i in range(1, len(velocities)):
            accel = velocities[i] - velocities[i-1]
            accelerations.append(accel)
        return accelerations


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
        # Lower blue range
        lower_blue1 = np.array([100, 50, 50])
        upper_blue1 = np.array([130, 255, 255])
        
        # Upper blue range (for different lighting)
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
    def __init__(self, device: Optional[str] = None, fps: float = 25.0):
        """Create detector object. Model is not loaded until load_model() is called.

        Args:
            device: torch device string, e.g. 'cpu' or 'cuda:0'. If None, let ultralytics pick.
            fps: Expected frames per second of the video stream for temporal analysis.
        """
        self.model = None
        self.device = device
        self.fps = fps
        
        # Detection history for temporal analysis
        self.detection_history = []
        self.max_history_frames = int(fps * 10)  # Keep 10 seconds of history
        
        # Drowning detection parameters
        self.drowning_config = {
            'min_detection_confidence': 0.5,
            'person_class_id': 0,  # COCO class ID for person
            'vertical_movement_threshold': 5.0,  # pixels per frame
            'horizontal_movement_threshold': 10.0,
            'struggling_motion_variance': 15.0,
            'immobile_time_threshold': 3.0,  # seconds
            'rapid_sinking_threshold': 20.0,  # pixels per frame downward
            'aspect_ratio_threshold': 0.3,  # width/height ratio indicating horizontal position
        }

    def load_model(self, model_path: str = "yolov8n.pt", enable_pose: bool = False) -> None:
        """Load a YOLO model from a local path or one of the Ultralytics short names.
        This call may download the model if not present locally.
        
        Args:
            model_path: Path to YOLO model or ultralytics model name
            enable_pose: Whether to also load pose estimation model
        """
        try:
            from ultralytics import YOLO
        except Exception as e:
            raise RuntimeError("ultralytics package is required. Install with pip install ultralytics") from e

        self.model = YOLO(model_path)
        if self.device:
            try:
                self.model.to(self.device)
            except Exception:
                # ultralytics will usually handle device selection; ignore on failure
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

    def predict_frame(self, frame) -> Tuple[List[Dict], np.ndarray]:
        """Run inference on a single frame and return detections with environmental context.

        Returns:
            Tuple of (detections_list, water_mask)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Detect water areas for context
        water_mask = None
        if self.drowning_config['water_detection_enabled']:
            water_mask = self.water_detector.detect_water_areas(frame)

        # Run YOLO detection
        results = self.model.predict(source=frame, imgsz=640, conf=0.25, verbose=False)
        
        # Run pose estimation if enabled
        pose_results = None
        if self.drowning_config['pose_estimation_enabled'] and self.pose_model:
            pose_results = self.pose_model.predict(source=frame, imgsz=640, conf=0.3, verbose=False)

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
                "bbox_stability": 1.0,  # Will be calculated in tracking
                "visibility_score": self._calculate_visibility_score(detection),
            }
            
            # Add pose information if available
            if pose_results and detection['class_id'] == 0:  # Person class
                pose_data = self._extract_pose_data(pose_results, detection)
                detection["pose"] = pose_data
            
            detections.append(detection)
        
        return detections, water_mask
    
    def _calculate_pool_distance(self, center_point: Tuple[float, float]) -> float:
        """Calculate distance from person to pool edge."""
        if self.water_detector.pool_boundaries is None:
            return 0.0
            
        point = np.array([[center_point[0], center_point[1]]], dtype=np.float32)
        distance = cv2.pointPolygonTest(self.water_detector.pool_boundaries, 
                                      (center_point[0], center_point[1]), True)
        return abs(distance)
    
    def _calculate_visibility_score(self, detection: Dict) -> float:
        """Calculate how visible/clear the person detection is."""
        # Based on confidence, size, and aspect ratio
        conf_score = detection['confidence']
        
        # Size factor (larger detections are generally more reliable)
        area = detection['area']
        size_score = min(area / 10000, 1.0)  # Normalize to reasonable person size
        
        # Aspect ratio factor (normal person ratios are more reliable)
        aspect_ratio = detection['aspect_ratio']
        normal_ratio_range = (0.3, 0.8)  # Typical person aspect ratios
        if normal_ratio_range[0] <= aspect_ratio <= normal_ratio_range[1]:
            ratio_score = 1.0
        else:
            ratio_score = max(0.3, 1.0 - abs(aspect_ratio - 0.5) * 2)
        
        return (conf_score * 0.5 + size_score * 0.3 + ratio_score * 0.2)
    
    def _extract_pose_data(self, pose_results, detection: Dict) -> Dict:
        """Extract pose keypoints and analyze body position."""
        pose_data = {
            "keypoints": [],
            "pose_confidence": 0.0,
            "head_above_water": True,
            "body_orientation": "vertical",  # vertical, horizontal, unknown
            "arm_position": "normal",        # normal, raised, struggling
            "stability_score": 1.0
        }
        
        if not pose_results or not pose_results[0].keypoints:
            return pose_data
            
        # Find pose data that corresponds to this detection
        det_center = np.array(detection['center'])
        
        for pose_result in pose_results[0].keypoints.data:
            if len(pose_result) >= 17:  # Standard COCO pose format
                # Calculate pose center from keypoints
                visible_points = pose_result[pose_result[:, 2] > 0.3]  # confidence > 0.3
                if len(visible_points) > 0:
                    pose_center = np.mean(visible_points[:, :2], axis=0)
                    distance = np.linalg.norm(det_center - pose_center)
                    
                    if distance < 50:  # Match pose to detection
                        pose_data["keypoints"] = pose_result.tolist()
                        pose_data["pose_confidence"] = float(np.mean(pose_result[:, 2]))
                        
                        # Analyze body orientation
                        pose_data.update(self._analyze_body_orientation(pose_result))
                        break
        
        return pose_data
    
    def _analyze_body_orientation(self, keypoints: np.ndarray) -> Dict:
        """Analyze body orientation from pose keypoints."""
        analysis = {
            "head_above_water": True,
            "body_orientation": "vertical",
            "arm_position": "normal",
            "stability_score": 1.0
        }
        
        # Key point indices (COCO format)
        nose_idx, left_shoulder_idx, right_shoulder_idx = 0, 5, 6
        left_hip_idx, right_hip_idx = 11, 12
        left_wrist_idx, right_wrist_idx = 9, 10
        
        try:
            # Check if key points are visible
            if (keypoints[nose_idx, 2] > 0.3 and 
                keypoints[left_shoulder_idx, 2] > 0.3 and 
                keypoints[right_shoulder_idx, 2] > 0.3):
                
                # Calculate body orientation
                shoulder_line = keypoints[right_shoulder_idx, :2] - keypoints[left_shoulder_idx, :2]
                shoulder_angle = np.arctan2(shoulder_line[1], shoulder_line[0]) * 180 / np.pi
                
                if abs(shoulder_angle) > 45:  # More horizontal than vertical
                    analysis["body_orientation"] = "horizontal"
                    analysis["stability_score"] *= 0.5  # Horizontal position is concerning
                
                # Check arm positions (struggling indicator)
                if (keypoints[left_wrist_idx, 2] > 0.3 and keypoints[right_wrist_idx, 2] > 0.3):
                    left_arm_y = keypoints[left_wrist_idx, 1]
                    right_arm_y = keypoints[right_wrist_idx, 1]
                    shoulder_y = (keypoints[left_shoulder_idx, 1] + keypoints[right_shoulder_idx, 1]) / 2
                    
                    if left_arm_y < shoulder_y - 20 or right_arm_y < shoulder_y - 20:
                        analysis["arm_position"] = "raised"
                        analysis["stability_score"] *= 0.7  # Raised arms can indicate distress
                
                # Head position analysis
                nose_y = keypoints[nose_idx, 1]
                if keypoints[left_shoulder_idx, 2] > 0.3:
                    shoulder_y = keypoints[left_shoulder_idx, 1]
                    if nose_y > shoulder_y + 10:  # Head below shoulders
                        analysis["head_above_water"] = False
                        analysis["stability_score"] *= 0.3
                        
        except (IndexError, TypeError):
            pass  # Use default values if pose analysis fails
            
        return analysis

    def update_detection_history(self, detections: List[Dict]) -> None:
        """Update the detection history with current frame detections."""
        # Filter for person detections with sufficient confidence
        person_detections = [
            d for d in detections 
            if d['class_id'] == self.drowning_config['person_class_id'] 
            and d['confidence'] >= self.drowning_config['min_detection_confidence']
        ]
        
        frame_data = {
            'timestamp': time.time(),
            'detections': person_detections,
            'person_count': len(person_detections)
        }
        
        self.detection_history.append(frame_data)
        
        # Maintain history size
        if len(self.detection_history) > self.max_history_frames:
            self.detection_history.pop(0)

    def track_person_movement(self, current_detection: Dict) -> Dict:
        """Track movement patterns of a person across frames."""
        movement_data = {
            'vertical_velocity': 0.0,
            'horizontal_velocity': 0.0,
            'acceleration': 0.0,
            'movement_variance': 0.0,
            'is_struggling': False,
            'is_sinking': False,
            'is_immobile': False
        }
        
        if len(self.detection_history) < 3:
            return movement_data
            
        # Find similar detections in recent history for tracking
        recent_frames = self.detection_history[-10:]  # Last 10 frames
        current_center = current_detection['center']
        
        # Find closest detection in previous frames (simple tracking)
        tracked_positions = []
        for frame in recent_frames:
            if frame['detections']:
                closest_detection = min(
                    frame['detections'],
                    key=lambda d: np.sqrt(
                        (d['center'][0] - current_center[0])**2 + 
                        (d['center'][1] - current_center[1])**2
                    )
                )
                distance = np.sqrt(
                    (closest_detection['center'][0] - current_center[0])**2 + 
                    (closest_detection['center'][1] - current_center[1])**2
                )
                if distance < 100:  # Only track if reasonably close
                    tracked_positions.append({
                        'center': closest_detection['center'],
                        'timestamp': frame['timestamp'],
                        'bbox': closest_detection['bbox']
                    })
        
        if len(tracked_positions) >= 2:
            # Calculate velocities
            positions = np.array([pos['center'] for pos in tracked_positions])
            times = np.array([pos['timestamp'] for pos in tracked_positions])
            
            # Vertical movement (positive = downward)
            vertical_positions = positions[:, 1]
            if len(vertical_positions) > 1:
                vertical_diff = np.diff(vertical_positions)
                time_diff = np.diff(times)
                vertical_velocities = vertical_diff / time_diff
                movement_data['vertical_velocity'] = np.mean(vertical_velocities)
                
                # Horizontal movement
                horizontal_positions = positions[:, 0]
                horizontal_diff = np.diff(horizontal_positions)
                horizontal_velocities = horizontal_diff / time_diff
                movement_data['horizontal_velocity'] = np.mean(horizontal_velocities)
                
                # Movement variance (indicates struggling)
                movement_data['movement_variance'] = np.var(vertical_velocities) + np.var(horizontal_velocities)
                
                # Detection flags
                movement_data['is_sinking'] = movement_data['vertical_velocity'] > self.drowning_config['rapid_sinking_threshold']
                movement_data['is_struggling'] = movement_data['movement_variance'] > self.drowning_config['struggling_motion_variance']
                movement_data['is_immobile'] = (
                    abs(movement_data['vertical_velocity']) < self.drowning_config['vertical_movement_threshold'] and
                    abs(movement_data['horizontal_velocity']) < self.drowning_config['horizontal_movement_threshold']
                )
        
        return movement_data

    def detect_body_position(self, detection: Dict) -> Dict:
        """Analyze body position from bounding box characteristics."""
        position_data = {
            'is_horizontal': False,
            'is_partially_submerged': False,
            'body_position_score': 0.0
        }
        
        # Horizontal position indicator (drowning persons often float horizontally)
        aspect_ratio = detection['aspect_ratio']
        position_data['is_horizontal'] = aspect_ratio < self.drowning_config['aspect_ratio_threshold']
        
        # Estimate submersion based on bbox height relative to normal standing person
        # This is a rough heuristic - in real scenarios you'd need water level detection
        normal_height_ratio = 1.5  # Typical standing person aspect ratio
        current_height_ratio = detection['height'] / detection['width']
        
        if current_height_ratio < normal_height_ratio * 0.6:
            position_data['is_partially_submerged'] = True
            
        # Calculate overall body position score (0 = normal, 1 = high drowning risk)
        score = 0.0
        if position_data['is_horizontal']:
            score += 0.4
        if position_data['is_partially_submerged']:
            score += 0.3
        if detection['confidence'] < 0.7:  # Lower confidence might indicate partial occlusion
            score += 0.2
            
        position_data['body_position_score'] = min(score, 1.0)
        
        return position_data

    def advanced_drowning_detection(self, current_detections: List[Dict], water_mask: np.ndarray = None) -> Dict:
        """
        State-of-the-art drowning detection using multiple AI techniques.
        
        Returns:
            Comprehensive detection results with confidence scores and analysis
        """
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
                'new_persons': 0,
                'lost_tracks': 0
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
        
        # Add contextual alerts
        self._add_contextual_alerts(result, tracks)
        
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
            'movement_analysis': {},
            'position_analysis': {},
            'temporal_analysis': {},
            'pose_analysis': {},
            'environmental_analysis': {}
        }
        
        # 1. Movement Analysis (Enhanced)
        movement = self._advanced_movement_analysis(track_data)
        analysis['movement_analysis'] = movement
        
        # 2. Position Analysis (Enhanced)
        position = self._advanced_position_analysis(current_detection, track_data)
        analysis['position_analysis'] = position
        
        # 3. Temporal Analysis (New)
        temporal = self._temporal_pattern_analysis(track_data)
        analysis['temporal_analysis'] = temporal
        
        # 4. Pose Analysis (New)
        if current_detection.get('pose') and self.drowning_config['pose_estimation_enabled']:
            pose = self._pose_based_analysis(current_detection['pose'])
            analysis['pose_analysis'] = pose
        
        # 5. Environmental Analysis (New)
        environmental = self._environmental_context_analysis(current_detection)
        analysis['environmental_analysis'] = environmental
        
        # 6. Calculate Overall Risk Score
        risk_components = {
            'movement_risk': movement.get('risk_score', 0.0) * 0.25,
            'position_risk': position.get('risk_score', 0.0) * 0.20,
            'temporal_risk': temporal.get('risk_score', 0.0) * 0.20,
            'pose_risk': pose.get('risk_score', 0.0) * 0.20 if 'pose' in analysis else 0.0,
            'environmental_risk': environmental.get('risk_score', 0.0) * 0.15
        }
        
        analysis['risk_score'] = min(sum(risk_components.values()), 1.0)
        
        # 7. Determine Risk Level and Alerts
        self._determine_risk_level_and_alerts(analysis, risk_components)
        
        return analysis
    
    def _advanced_movement_analysis(self, track_data: Dict) -> Dict:
        """Advanced movement pattern analysis."""
        movement = {
            'risk_score': 0.0,
            'velocity_patterns': [],
            'acceleration_patterns': [],
            'movement_consistency': 1.0,
            'struggling_indicators': [],
            'sinking_rate': 0.0,
            'immobility_duration': 0.0
        }
        
        if len(track_data['positions']) < 3:
            return movement
        
        positions = np.array(list(track_data['positions']))
        velocities = list(track_data['velocities'])
        
        # Calculate movement statistics
        if len(velocities) > 1:
            velocity_mean = np.mean(velocities)
            velocity_std = np.std(velocities)
            movement['movement_consistency'] = max(0.0, 1.0 - velocity_std / max(velocity_mean, 1.0))
            
            # Detect struggling (high velocity variance)
            if velocity_std > self.drowning_config['struggling_motion_variance']:
                movement['struggling_indicators'].append('high_velocity_variance')
                movement['risk_score'] += 0.3
            
            # Calculate sinking rate (vertical movement)
            if len(positions) >= 5:
                recent_positions = positions[-5:]
                vertical_trend = np.polyfit(range(len(recent_positions)), recent_positions[:, 1], 1)[0]
                movement['sinking_rate'] = max(0, vertical_trend)  # Positive = sinking
                
                if vertical_trend > self.drowning_config['rapid_sinking_threshold']:
                    movement['struggling_indicators'].append('rapid_sinking')
                    movement['risk_score'] += 0.4
            
            # Detect immobility
            recent_velocities = velocities[-10:] if len(velocities) >= 10 else velocities
            if all(v < self.drowning_config['vertical_movement_threshold'] for v in recent_velocities):
                movement['immobility_duration'] = len(recent_velocities) / self.fps
                if movement['immobility_duration'] > self.drowning_config['immobile_time_threshold']:
                    movement['struggling_indicators'].append('prolonged_immobility')
                    movement['risk_score'] += 0.35
        
        return movement
    
    def _advanced_position_analysis(self, detection: Dict, track_data: Dict) -> Dict:
        """Enhanced body position analysis."""
        position = {
            'risk_score': 0.0,
            'orientation': 'vertical',
            'submersion_indicators': [],
            'size_consistency': 1.0,
            'visibility_trend': 1.0
        }
        
        # Aspect ratio analysis
        aspect_ratio = detection['aspect_ratio']
        if aspect_ratio < self.drowning_config['aspect_ratio_threshold']:
            position['orientation'] = 'horizontal'
            position['submersion_indicators'].append('horizontal_orientation')
            position['risk_score'] += 0.4
        
        # Size consistency analysis
        if len(track_data['detections']) > 5:
            recent_areas = [d['area'] for d in list(track_data['detections'])[-5:]]
            area_std = np.std(recent_areas)
            area_mean = np.mean(recent_areas)
            position['size_consistency'] = max(0.0, 1.0 - area_std / max(area_mean, 1.0))
            
            if position['size_consistency'] < 0.5:
                position['submersion_indicators'].append('unstable_detection_size')
                position['risk_score'] += 0.2
        
        # Visibility trend analysis
        if len(track_data['detections']) > 3:
            recent_confidences = [d['confidence'] for d in list(track_data['detections'])[-3:]]
            confidence_trend = np.polyfit(range(len(recent_confidences)), recent_confidences, 1)[0]
            
            if confidence_trend < -self.drowning_config['submersion_confidence_drop']:
                position['submersion_indicators'].append('decreasing_visibility')
                position['risk_score'] += 0.3
        
        return position
    
    def _temporal_pattern_analysis(self, track_data: Dict) -> Dict:
        """Analyze temporal patterns in behavior."""
        temporal = {
            'risk_score': 0.0,
            'behavior_patterns': [],
            'consistency_score': 1.0,
            'distress_duration': 0.0
        }
        
        if len(track_data['detections']) < 10:
            return temporal
        
        # Analyze behavior consistency over time
        recent_detections = list(track_data['detections'])[-20:]  # Last 20 frames
        
        # Calculate pattern stability
        confidence_pattern = [d['confidence'] for d in recent_detections]
        position_pattern = [d['center'][1] for d in recent_detections]  # Y-coordinates
        
        confidence_stability = 1.0 - np.std(confidence_pattern) / max(np.mean(confidence_pattern), 0.1)
        position_stability = 1.0 - np.std(position_pattern) / max(np.mean(position_pattern), 1.0)
        
        temporal['consistency_score'] = (confidence_stability + position_stability) / 2
        
        if temporal['consistency_score'] < 0.6:
            temporal['behavior_patterns'].append('erratic_behavior')
            temporal['risk_score'] += 0.25
        
        # Calculate duration of distress indicators
        distress_frames = 0
        for detection in recent_detections:
            if (detection['confidence'] < 0.5 or 
                detection['aspect_ratio'] < self.drowning_config['aspect_ratio_threshold']):
                distress_frames += 1
        
        temporal['distress_duration'] = distress_frames / self.fps
        if temporal['distress_duration'] > self.drowning_config['distress_time_threshold']:
            temporal['behavior_patterns'].append('sustained_distress')
            temporal['risk_score'] += 0.3
        
        return temporal
    
    def _pose_based_analysis(self, pose_data: Dict) -> Dict:
        """Analyze body pose for drowning indicators."""
        pose = {
            'risk_score': 0.0,
            'pose_indicators': [],
            'body_stability': pose_data.get('stability_score', 1.0)
        }
        
        # Head position analysis
        if not pose_data.get('head_above_water', True):
            pose['pose_indicators'].append('head_submerged')
            pose['risk_score'] += 0.5
        
        # Body orientation
        if pose_data.get('body_orientation') == 'horizontal':
            pose['pose_indicators'].append('horizontal_body')
            pose['risk_score'] += 0.4
        
        # Arm position (struggling indicator)
        if pose_data.get('arm_position') == 'raised':
            pose['pose_indicators'].append('arms_raised_distress')
            pose['risk_score'] += 0.3
        
        # Overall pose confidence
        if pose_data.get('pose_confidence', 1.0) < 0.3:
            pose['pose_indicators'].append('unclear_pose')
            pose['risk_score'] += 0.2
        
        return pose
    
    def _environmental_context_analysis(self, detection: Dict) -> Dict:
        """Analyze environmental context."""
        environmental = {
            'risk_score': 0.0,
            'context_factors': [],
            'water_proximity': True
        }
        
        # Water proximity
        if not detection.get('in_water', True):
            environmental['water_proximity'] = False
            environmental['risk_score'] = 0.0  # Not in water = no drowning risk
            return environmental
        
        # Distance to pool edge
        edge_distance = detection.get('distance_to_pool_edge', 0)
        if edge_distance < self.drowning_config['pool_edge_safety_margin']:
            environmental['context_factors'].append('near_pool_edge')
            environmental['risk_score'] += 0.1
        
        # Detection size (person might be partially submerged if small)
        if detection['area'] < self.drowning_config['minimum_person_size']:
            environmental['context_factors'].append('small_detection_size')
            environmental['risk_score'] += 0.2
        
        return environmental
    
    def _determine_risk_level_and_alerts(self, analysis: Dict, risk_components: Dict) -> None:
        """Determine final risk level and generate appropriate alerts."""
        risk_score = analysis['risk_score']
        alerts = analysis['alerts']
        
        # Determine risk level
        if risk_score >= self.drowning_config['critical_risk_threshold']:
            analysis['risk_level'] = 'critical'
            alerts.append("CRITICAL: Immediate intervention required!")
        elif risk_score >= self.drowning_config['high_risk_threshold']:
            analysis['risk_level'] = 'high'
            alerts.append("HIGH RISK: Close monitoring required")
        elif risk_score >= self.drowning_config['medium_risk_threshold']:
            analysis['risk_level'] = 'medium'
            alerts.append("Medium risk detected")
        else:
            analysis['risk_level'] = 'low'
        
        # Add specific alerts based on analysis components
        movement = analysis['movement_analysis']
        for indicator in movement.get('struggling_indicators', []):
            if indicator == 'rapid_sinking':
                alerts.append("Person appears to be sinking rapidly")
            elif indicator == 'high_velocity_variance':
                alerts.append("Erratic movement patterns detected")
            elif indicator == 'prolonged_immobility':
                alerts.append(f"Person immobile for {movement['immobility_duration']:.1f} seconds")
        
        position = analysis['position_analysis']
        for indicator in position.get('submersion_indicators', []):
            if indicator == 'horizontal_orientation':
                alerts.append("Person in horizontal position")
            elif indicator == 'decreasing_visibility':
                alerts.append("Person becoming less visible (possible submersion)")
        
        if analysis.get('pose_analysis'):
            pose_indicators = analysis['pose_analysis'].get('pose_indicators', [])
            if 'head_submerged' in pose_indicators:
                alerts.append("Head appears to be below water level")
            if 'arms_raised_distress' in pose_indicators:
                alerts.append("Arms raised in possible distress signal")
    
    def _add_contextual_alerts(self, result: Dict, tracks: Dict) -> None:
        """Add contextual alerts based on overall scene analysis."""
        # Multiple person interactions
        if len(tracks) > 1:
            high_risk_count = sum(1 for p in result['person_analyses'] if p['risk_level'] in ['high', 'critical'])
            if high_risk_count > 1:
                result['alerts'].append(f"Multiple persons ({high_risk_count}) showing distress")
        
        # Environmental alerts
        if not result['environmental_context']['water_detected']:
            result['alerts'].append("Water area detection failed - manual verification recommended")

    # Legacy methods for backward compatibility
    def update_detection_history(self, detections: List[Dict]) -> None:
        """Legacy method - now handled by PersonTracker."""
        pass
    
    def track_person_movement(self, current_detection: Dict) -> Dict:
        """Legacy method - redirects to advanced movement analysis."""
        # Create minimal track data for compatibility
        track_data = {
            'positions': deque([current_detection['center']], maxlen=50),
            'detections': deque([current_detection], maxlen=50),
            'velocities': deque(maxlen=49),
        }
        
        movement = self._advanced_movement_analysis(track_data)
        
        # Convert to legacy format
        return {
            'vertical_velocity': movement.get('sinking_rate', 0.0),
            'horizontal_velocity': 0.0,
            'acceleration': 0.0,
            'movement_variance': 1.0 - movement.get('movement_consistency', 1.0),
            'is_struggling': len(movement.get('struggling_indicators', [])) > 0,
            'is_sinking': 'rapid_sinking' in movement.get('struggling_indicators', []),
            'is_immobile': 'prolonged_immobility' in movement.get('struggling_indicators', [])
        }
    
    def detect_body_position(self, detection: Dict) -> Dict:
        """Legacy method - redirects to advanced position analysis."""
        track_data = {'detections': deque([detection], maxlen=50)}
        position = self._advanced_position_analysis(detection, track_data)
        
        # Convert to legacy format
        return {
            'is_horizontal': position['orientation'] == 'horizontal',
            'is_partially_submerged': len(position.get('submersion_indicators', [])) > 0,
            'body_position_score': position.get('risk_score', 0.0)
        }
    
    def get_immobile_duration(self, current_detection: Dict) -> float:
        """Legacy method - returns estimated immobility duration."""
        return 0.0  # Would need full tracking history
    
    def comprehensive_drowning_detection(self, current_detections: List[Dict]) -> Dict:
        """Legacy method - redirects to advanced detection system."""
        # Convert detections to new format if needed
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
        
        # Use the advanced detection system
        current_detections = history[-1].get('detections', []) if history else []
        result = self.advanced_drowning_detection(current_detections)
        return result['drowning_detected']

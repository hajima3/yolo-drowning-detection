"""
Simple wrapper around Ultralytics YOLO for person detection and a place to implement
pool-specific drowning heuristics.
"""
from typing import Optional, List, Dict


class DrowningDetector:
    def __init__(self, device: Optional[str] = None):
        """Create detector object. Model is not loaded until load_model() is called.

        Args:
            device: torch device string, e.g. 'cpu' or 'cuda:0'. If None, let ultralytics pick.
        """
        self.model = None
        self.device = device

    def load_model(self, model_path: str = "yolov8n.pt") -> None:
        """Load a YOLO model from a local path or one of the Ultralytics short names.
        This call may download the model if not present locally.
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

    def predict_frame(self, frame) -> List[Dict]:
        """Run inference on a single frame (numpy array / image path) and return list of detections.

        Each detection dict contains: class_id, name, confidence, bbox (xmin,ymin,xmax,ymax)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        results = self.model.predict(source=frame, imgsz=640, conf=0.25, verbose=False)
        # ultralytics returns a list of Results; we handle first item
        if not results:
            return []
        r = results[0]
        detections = []
        for det in r.boxes.data.tolist() if hasattr(r.boxes, 'data') else []:
            # r.boxes.data rows: [xmin, ymin, xmax, ymax, score, class]
            xmin, ymin, xmax, ymax, score, cls = det[:6]
            detections.append({
                "class_id": int(cls),
                "name": r.names[int(cls)] if hasattr(r, 'names') else str(int(cls)),
                "confidence": float(score),
                "bbox": [float(xmin), float(ymin), float(xmax), float(ymax)],
            })
        return detections

    def simple_drowning_heuristic(self, history: List[Dict]) -> bool:
        """Placeholder heuristic: decides drowning-like condition from recent detection history.

        history: list of per-frame summaries (e.g., presence/absence, bbox sizes, motion metrics)
        Returns True when a possible drowning is detected and needs escalation.

        Note: This is a stub. Replace with a tested heuristic using pose estimation + temporal rules.
        """
        # Edge case: empty history
        if not history:
            return False

        # Example rule (very naive): if a person is detected but shows near-zero vertical movement
        # for N consecutive frames, flag it. This requires preprocessing to fill 'motion' values.
        stuck_frames = sum(1 for h in history if h.get('motion', 0) < 0.01 and h.get('in_water', True))
        if stuck_frames >= 50:  # ~50 frames (adjust based on fps -> ~2 seconds at 25fps)
            return True
        return False

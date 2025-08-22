"""
Small CLI to run inference on a video file or camera stream for manual testing.
"""
import argparse
import time

from src.drowning_detector import DrowningDetector
import cv2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', '-s', default=0, help='Path to video file or camera index or RTSP url')
    parser.add_argument('--model', '-m', default='yolov8n.pt', help='Model path or ultralytics short name')
    parser.add_argument('--show', action='store_true', help='Show video with detections')
    args = parser.parse_args()

    det = DrowningDetector()
    det.load_model(args.model)

    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print('Failed to open source:', args.source)
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    print('Source opened, FPS:', fps)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        t0 = time.time()
        dets = det.predict_frame(frame)
        t1 = time.time()
        if args.show:
            for d in dets:
                xmin, ymin, xmax, ymax = map(int, d['bbox'])
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(frame, f"{d['name']} {d['confidence']:.2f}", (xmin, max(ymin-6,0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            cv2.imshow('inference', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print(f'Frame processed in {(t1-t0)*1000:.1f} ms, detections:', len(dets))
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

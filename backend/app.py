"""
Flask Backend API for Object Detection System (improved, color-fix)
- Ensures webcam frames are color (BGR) before processing/streaming
- Robust webcam handling (select camera index, warm up, drop old frames)
- Thread-safe detection loop
- Proper handling of ultralytics YOLO results
- CPU / CUDA device selection at startup
- Endpoints: start, stop, status, video-feed, set confidence, set camera index,
             list available cameras, save frame, saved frames management
"""

from flask import Flask, Response, jsonify, request, send_from_directory
from flask_cors import CORS
import cv2
from ultralytics import YOLO
import numpy as np
import json
import time
import os
from datetime import datetime
from pathlib import Path
import threading
from collections import defaultdict, deque
import atexit
import logging
import torch

# ---------- Configuration ----------
DEFAULT_CAMERA_INDEX = int(os.environ.get("CAM_INDEX", 0))
MAX_CAMERA_TEST_INDEX = 5  # used for listing available cameras
FRAME_WIDTH = int(os.environ.get("FRAME_WIDTH", 640))
FRAME_HEIGHT = int(os.environ.get("FRAME_HEIGHT", 480))
TARGET_FPS = int(os.environ.get("TARGET_FPS", 30))
SAVED_FRAMES_DIR = Path(__file__).parent / "saved_frames"
SAVED_FRAMES_DIR.mkdir(exist_ok=True)

# ---------- App & logging ----------
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:5000",
            "https://object-detection-2-9oo8.onrender.com",
            "https://object-detection-rirh.onrender.com"
        ]
    }
})
logging.basicConfig(level=logging.INFO)

# ---------- Global state ----------
camera = None
camera_index = DEFAULT_CAMERA_INDEX
model = None
device = "cpu"
detection_active = False
detection_thread = None

frame_lock = threading.Lock()
current_frame = None  # BGR numpy array
fps_queue = deque(maxlen=30)

# Metrics
current_metrics = {
    "fps": 0.0,
    "confidence": 0.15,
    "object_count": 0,
    "frames_processed": 0,
    "saved_count": 0,
    "detections": {},
    "session_start": None,
}

# ---------- Utilities ----------

def get_color_for_class(class_name: str):
    """Return consistent BGR color for given class name."""
    base_colors = {
        "person": (255, 100, 100),
        "car": (100, 255, 100),
        "truck": (100, 200, 255),
        "bus": (255, 100, 200),
        "motorcycle": (200, 100, 255),
        "bicycle": (100, 255, 255),
    }
    if class_name in base_colors:
        return base_colors[class_name]
    # deterministic hash-based color
    h = abs(hash(class_name))
    r = (h & 0xFF0000) >> 16
    g = (h & 0x00FF00) >> 8
    b = (h & 0x0000FF)
    # brighten
    r = min(255, r + 80)
    g = min(255, g + 80)
    b = min(255, b + 80)
    return (b, g, r)

def safe_imencode_jpeg(frame, quality=85):
    """Encode frame to JPEG bytes in a safe way (thread-safe)."""
    ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ret:
        return None
    return buffer.tobytes()

def is_color_frame(frame: np.ndarray) -> bool:
    """Return True if frame is multi-channel color (3 or 4 channels)."""
    if frame is None:
        return False
    # grayscale: ndim == 2
    if frame.ndim == 2:
        return False
    # color-like: ndim == 3 and channels >= 3
    if frame.ndim == 3 and frame.shape[2] >= 3:
        return True
    return False

def normalize_frame_to_bgr(frame: np.ndarray) -> np.ndarray:
    """
    Ensure frame is BGR with 3 channels.
    - If Gray -> convert to BGR (will still be grayscale visually but consistent)
    - If BGRA -> convert to BGR
    """
    if frame is None:
        return None
    if frame.ndim == 2:
        # Single channel -> convert to BGR
        return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    if frame.ndim == 3 and frame.shape[2] == 4:
        # BGRA -> BGR
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    # already BGR (3 channels)
    return frame

# ---------- Model loading ----------

def load_model(weights_path: str = "yolov8m.pt", prefer_gpu: bool = True):
    """Load ultralytics YOLO model and move to device (cuda if available)."""
    global model, device
    try:
        logging.info("Loading YOLO model...")
        
        # Add safe globals for PyTorch 2.6+ compatibility
        import torch.serialization
        try:
            # Allow ultralytics classes for torch.load
            from ultralytics.nn.tasks import DetectionModel
            torch.serialization.add_safe_globals([DetectionModel])
        except Exception as safe_global_err:
            logging.warning(f"Could not add safe globals (non-critical): {safe_global_err}")
        
        # Try loading model
        try:
            model = YOLO(weights_path)
        except Exception as load_err:
            # Fallback: Try downloading fresh weights if local file fails
            logging.warning(f"Failed to load local weights, trying to download: {load_err}")
            model = YOLO("yolov8m.pt")  # This will auto-download if needed
        
        # choose device
        if prefer_gpu and torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        # move model to device if supported
        try:
            model.to(device)
        except Exception:
            # some ultralytics versions handle device in predict call; ignore if .to not supported
            pass
        logging.info(f"Model loaded ({weights_path}) on device: {device}")
        return True
    except Exception as e:
        logging.exception("Failed to load model")
        model = None
        return False

# Try loading default weights
load_model()

# ---------- Camera control ----------

def open_camera(index: int = 0, warmup_seconds: float = 0.5, try_mjpg: bool = True) -> bool:
    """
    Open the camera, set properties, and flush buffer to reduce latency.
    Performs a quick color-check. If frame appears grayscale, it will attempt reopening
    without forcing MJPG/FourCC to allow proper color frames.
    """
    global camera, camera_index
    camera_index = index
    if camera is not None:
        try:
            camera.release()
        except Exception:
            pass
        camera = None

    # Choose backend: DirectShow on Windows often works better
    backend_args = {}
    try_mjpg_local = try_mjpg

    def try_open(use_fourcc: bool):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW) if os.name == "nt" else cv2.VideoCapture(index)
        if not cap or not cap.isOpened():
            return None
        # recommended properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
        # Encourage conversion to RGB where supported
        try:
            cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)
        except Exception:
            pass
        # try to reduce buffer size (may be ignored)
        try:
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception:
            pass
        if use_fourcc:
            try:
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            except Exception:
                pass
        return cap

    # First attempt: with MJPG (many webcams benefit)
    cap = try_open(use_fourcc=try_mjpg_local)
    if cap is None or not cap.isOpened():
        logging.warning(f"Camera index {index} could not be opened on first attempt.")
        return False

    # warm-up: read a few frames and drop them (reduces initial lag)
    t0 = time.time()
    last_frame = None
    while time.time() - t0 < warmup_seconds:
        ret, last_frame = cap.read()
        if not ret:
            break

    # if we got a last_frame, check whether it's color; if not, try reopening without FOURCC
    if last_frame is not None:
        if not is_color_frame(last_frame):
            logging.warning("Captured warm-up frame appears non-color (grayscale). Retrying without forcing FOURCC...")
            try:
                cap.release()
            except Exception:
                pass
            # Try without forcing FOURCC (some drivers prefer default)
            cap = try_open(use_fourcc=False)
            if cap is None or not cap.isOpened():
                logging.error("Reopen without FOURCC failed.")
                return False
            # warm-up again
            t0 = time.time()
            last_frame = None
            while time.time() - t0 < warmup_seconds:
                ret, last_frame = cap.read()
                if not ret:
                    break

    # Ensure we have at least one readable frame and normalize it
    if last_frame is None:
        # attempt one read to validate
        ret, last_frame = cap.read()
    if last_frame is None:
        logging.warning("Camera opened but no frames received.")
        try:
            cap.release()
        except Exception:
            pass
        return False

    # Normalize frame channels if necessary
    last_frame = normalize_frame_to_bgr(last_frame)

    camera = cap
    logging.info(f"Camera {index} opened (w:{FRAME_WIDTH}, h:{FRAME_HEIGHT}, fps:{TARGET_FPS}) - color_ok: {is_color_frame(last_frame)}")
    return True

def close_camera():
    global camera
    if camera:
        try:
            camera.release()
        except Exception:
            pass
        camera = None
        logging.info("Camera released")

def list_available_cameras(max_index=MAX_CAMERA_TEST_INDEX):
    """Try opening camera indices to see which are available (non-blocking, quick)."""
    available = []
    for i in range(0, max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) if os.name == "nt" else cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            try:
                cap.release()
            except Exception:
                pass
            continue
        # try reading one frame quickly
        ret, _ = cap.read()
        if ret:
            available.append(i)
        try:
            cap.release()
        except Exception:
            pass
    return available

# ---------- Detection loop ----------

def detection_loop(skip_frames: int = 0):
    """Threaded detection loop. If skip_frames > 0, runs detection once per (skip_frames+1) frames."""
    global detection_active, current_frame, current_metrics, fps_queue, camera, model

    if model is None:
        logging.error("No model loaded. Cannot start detection.")
        detection_active = False
        return

    # ensure camera opened
    if camera is None or not camera.isOpened():
        ok = open_camera(camera_index)
        if not ok:
            logging.error("Failed to open camera in detection loop.")
            detection_active = False
            return

    current_metrics["session_start"] = datetime.now().isoformat()
    current_metrics["frames_processed"] = 0
    frame_counter = 0
    last_time = time.time()

    # warm-up model once (optional small dummy inference to allocate GPU memory)
    try:
        # small black box
        dummy = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
        _ = model(dummy, conf=0.001, device=device)  # a tiny run to warm up
    except Exception:
        pass

    while detection_active:
        ret, frame = camera.read()
        if not ret or frame is None:
            # small sleep to avoid busy loop if camera fails momentarily
            time.sleep(0.01)
            continue

        # Normalize channel layout (ensure BGR 3-channel)
        frame = normalize_frame_to_bgr(frame)

        frame_counter += 1

        # reduce CPU work by optionally skipping frames
        if skip_frames > 0 and (frame_counter % (skip_frames + 1) != 0):
            # still update current_frame for streaming but skip detection
            with frame_lock:
                current_frame = frame.copy()
            continue

        try:
            # run inference
            confidence = current_metrics.get("confidence", 0.15)
            # call model on frame. Some ultralytics versions accept device in call, others don't.
            results = model(frame, conf=confidence, iou=0.45, max_det=200)
            # results is a list-like object (per batch). We only passed single frame -> iterate results
            detections_count = defaultdict(int)

            # draw boxes on a copy so we keep original intact
            out_frame = frame.copy()

            for res in results:
                # res.boxes contains bounding boxes
                boxes = res.boxes
                # convert to numpy arrays (if tensors)
                # boxes.xyxy -> Nx4
                xyxy = boxes.xyxy.cpu().numpy() if hasattr(boxes.xyxy, "cpu") else np.array(boxes.xyxy)
                confs = boxes.conf.cpu().numpy() if hasattr(boxes.conf, "cpu") else np.array(boxes.conf)
                cls_ids = boxes.cls.cpu().numpy().astype(int) if hasattr(boxes.cls, "cpu") else np.array(boxes.cls).astype(int)

                for (x1, y1, x2, y2), conf_val, cls_id in zip(xyxy, confs, cls_ids):
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    class_name = model.names[int(cls_id)] if model and hasattr(model, "names") else str(int(cls_id))
                    detections_count[class_name] += 1

                    color = get_color_for_class(class_name)

                    # rectangle
                    cv2.rectangle(out_frame, (x1, y1), (x2, y2), color, 2)

                    # label background
                    label = f"{class_name} {float(conf_val):.2f}"
                    (tw, th), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                    # ensure label within frame bounds
                    ly1 = max(0, y1 - th - 8)
                    ly2 = y1
                    lx1 = x1
                    lx2 = x1 + tw + 6
                    cv2.rectangle(out_frame, (lx1, ly1), (lx2, ly2), color, -1)
                    cv2.putText(out_frame, label, (x1 + 3, y1 - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

            # calculate fps
            now = time.time()
            delta = now - last_time if last_time else 0.000001
            last_time = now
            fps = 1.0 / delta if delta > 0 else 0
            fps_queue.append(fps)
            avg_fps = sum(fps_queue) / len(fps_queue) if len(fps_queue) else fps

            # update metrics
            current_metrics["fps"] = round(avg_fps, 2)
            current_metrics["object_count"] = sum(detections_count.values())
            current_metrics["detections"] = dict(detections_count)
            current_metrics["frames_processed"] += 1

            # save frame for streaming
            with frame_lock:
                current_frame = out_frame

        except Exception as e:
            logging.exception(f"Error in detection loop: {e}")
            # still keep the raw frame for streaming
            with frame_lock:
                current_frame = frame.copy()
            # small pause so logging doesn't spam
            time.sleep(0.01)
            continue

    # loop end -> release camera
    close_camera()

# ---------- Flask endpoints ----------

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "active": detection_active,
        "camera_index": camera_index,
        "camera_open": (camera is not None and camera.isOpened()) if camera else False,
        "model_loaded": model is not None,
        "device": device,
        "metrics": current_metrics
    })

@app.route("/api/list-cameras", methods=["GET"])
def api_list_cameras():
    cams = list_available_cameras()
    return jsonify({"available": cams})

@app.route("/api/set-camera", methods=["POST"])
def api_set_camera():
    global camera_index
    data = request.get_json() or {}
    idx = data.get("index")
    try:
        idx = int(idx)
    except Exception:
        return jsonify({"error": "invalid index"}), 400

    # if detection running, stop it first
    if detection_active:
        return jsonify({"error": "stop detection before changing camera"}), 409

    ok = open_camera(idx)
    if not ok:
        return jsonify({"error": f"could not open camera {idx}"}), 500
    camera_index = idx
    return jsonify({"status": "ok", "camera_index": idx})

@app.route("/api/start", methods=["POST"])
def api_start():
    global detection_active, detection_thread
    if detection_active:
        return jsonify({"status": "already_running"}), 200
    if model is None:
        return jsonify({
            "error": "Model not loaded. The YOLO model failed to initialize on this server."
        }), 500

    # ensure camera open
    ok = open_camera(camera_index)
    if not ok:
        return jsonify({
            "error": "Camera not available",
            "details": "This server doesn't have a physical camera. Camera-based detection only works when running the backend locally with a webcam.",
            "suggestion": "Run 'python app.py' locally in the backend folder to use camera features."
        }), 503  # 503 Service Unavailable is more appropriate than 500

    detection_active = True
    detection_thread = threading.Thread(target=detection_loop, kwargs={"skip_frames": 0}, daemon=True)
    detection_thread.start()
    return jsonify({"status": "started"})

@app.route("/api/stop", methods=["POST"])
def api_stop():
    global detection_active, detection_thread
    if not detection_active:
        return jsonify({"status": "already_stopped"}), 200
    detection_active = False
    if detection_thread is not None and detection_thread.is_alive():
        detection_thread.join(timeout=2)
    return jsonify({"status": "stopped"})

@app.route("/api/metrics", methods=["GET"])
def api_metrics():
    return jsonify(current_metrics)

@app.route("/api/confidence", methods=["POST"])
def api_set_confidence():
    data = request.get_json() or {}
    try:
        conf = float(data.get("confidence", current_metrics["confidence"]))
    except Exception:
        return jsonify({"error": "invalid confidence value"}), 400
    conf = max(0.01, min(0.99, conf))
    current_metrics["confidence"] = conf
    return jsonify({"confidence": conf})

@app.route("/api/video-feed")
def video_feed():
    """HTTP MJPEG streaming endpoint for the annotated frames."""
    boundary = "--frame"

    def generate():
        while True:
            if current_frame is None:
                time.sleep(0.01)
                continue
            with frame_lock:
                frame = current_frame.copy()
            # ensure frame is BGR and 3-channel before encoding
            frame = normalize_frame_to_bgr(frame)
            jpg = safe_imencode_jpeg(frame, quality=85)
            if jpg is None:
                time.sleep(0.01)
                continue
            yield (b"%s\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n" % (boundary.encode(), len(jpg))) + jpg + b"\r\n"
            # throttle to avoid excess CPU — desired ~30fps (adjust as needed)
            time.sleep(1.0 / max(1, TARGET_FPS))

    return Response(generate(), mimetype=f"multipart/x-mixed-replace; boundary={boundary}")

@app.route("/api/save-frame", methods=["POST"])
def api_save_frame():
    global current_metrics
    if current_frame is None:
        return jsonify({"error": "No frame available"}), 400
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"detection_{ts}_f{current_metrics['frames_processed']}.jpg"
        fpath = SAVED_FRAMES_DIR / fname
        with frame_lock:
            cv2.imwrite(str(fpath), current_frame)
        current_metrics["saved_count"] += 1
        return jsonify({"status": "saved", "filename": fname})
    except Exception as e:
        logging.exception("Failed to save frame")
        return jsonify({"error": str(e)}), 500

@app.route("/api/process-frame", methods=["POST"])
def api_process_frame():
    """
    Process a single frame sent from the frontend browser camera.
    This enables WebRTC-style detection where the browser captures the camera
    and sends frames to the backend for processing.
    """
    global current_metrics
    
    # Track FPS for browser camera mode
    import time
    start_time = time.time()
    
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        # Get uploaded frame
        if 'frame' not in request.files:
            return jsonify({"error": "No frame provided"}), 400
        
        file = request.files['frame']
        
        # Read image data
        file_bytes = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        # Process frame with YOLO
        conf_thresh = current_metrics.get("confidence", 0.15)
        results = model.predict(frame, conf=conf_thresh, verbose=False)
        
        # Draw detections on frame
        out_frame = frame.copy()
        detections_count = defaultdict(int)
        
        for result in results:
            boxes = result.boxes
            if boxes is None or len(boxes) == 0:
                continue
            
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                
                detections_count[class_name] += 1
                
                # Draw bounding box and label
                color = get_color_for_class(class_name)
                cv2.rectangle(out_frame, (x1, y1), (x2, y2), color, 2)
                
                label = f"{class_name} {conf:.2f}"
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                ly1 = max(y1 - th - 10, 0)
                ly2 = y1
                lx1 = x1
                lx2 = x1 + tw + 6
                cv2.rectangle(out_frame, (lx1, ly1), (lx2, ly2), color, -1)
                cv2.putText(out_frame, label, (x1 + 3, y1 - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Calculate FPS
        processing_time = time.time() - start_time
        fps = 1.0 / processing_time if processing_time > 0 else 0
        fps_queue.append(fps)
        avg_fps = sum(fps_queue) / len(fps_queue) if len(fps_queue) else fps
        
        # Update metrics
        current_metrics["fps"] = round(avg_fps, 2)
        current_metrics["object_count"] = sum(detections_count.values())
        current_metrics["detections"] = dict(detections_count)
        current_metrics["frames_processed"] += 1
        
        # Initialize session_start if not set
        if current_metrics.get("session_start") is None:
            current_metrics["session_start"] = datetime.now().isoformat()
        
        # Save processed frame for potential save-frame API
        with frame_lock:
            current_frame = out_frame
        
        logging.info(f"Frame processed: {current_metrics['frames_processed']}, "
                    f"FPS: {current_metrics['fps']}, "
                    f"Objects: {current_metrics['object_count']}")
        
        # Encode processed frame as JPEG
        ret, buffer = cv2.imencode('.jpg', out_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ret:
            return jsonify({"error": "Failed to encode frame"}), 500
        
        # Return processed frame
        return Response(
            buffer.tobytes(),
            mimetype='image/jpeg',
            headers={'Cache-Control': 'no-cache'}
        )
        
    except Exception as e:
        logging.exception("Error processing frame")
        return jsonify({"error": str(e)}), 500

@app.route("/api/saved-frames", methods=["GET"])
def api_saved_frames():
    frames = []
    for p in sorted(SAVED_FRAMES_DIR.glob("*.jpg"), reverse=True):
        st = p.stat()
        frames.append({
            "filename": p.name,
            "size": st.st_size,
            "created": datetime.fromtimestamp(st.st_ctime).isoformat(),
            "url": f"/api/saved-frames/{p.name}"
        })
    return jsonify({"frames": frames})

@app.route("/api/saved-frames/<filename>", methods=["GET"])
def api_get_saved_frame(filename):
    try:
        return send_from_directory(SAVED_FRAMES_DIR, filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/api/delete-frame/<filename>", methods=["DELETE"])
def api_delete_frame(filename):
    try:
        p = SAVED_FRAMES_DIR / filename
        if p.exists():
            p.unlink()
            return jsonify({"status": "deleted"})
        return jsonify({"error": "not found"}), 404
    except Exception as e:
        logging.exception("Error deleting file")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    """Root endpoint - API information"""
    return jsonify({
        "name": "Object Detection API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "metrics": "/api/metrics",
            "start_detection": "/api/start",
            "stop_detection": "/api/stop",
            "video_feed": "/api/video-feed",
            "saved_frames": "/api/saved-frames"
        },
        "frontend": "https://object-detection-2-9oo8.onrender.com",
        "documentation": "See frontend for full interface"
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# ---------- Cleanup on exit ----------
def shutdown():
    global detection_active
    logging.info("Shutting down server, cleaning resources...")
    detection_active = False
    try:
        if detection_thread is not None and detection_thread.is_alive():
            detection_thread.join(timeout=1)
    except Exception:
        pass
    close_camera()

atexit.register(shutdown)

# ---------- Start server ----------
if __name__ == "__main__":
    logging.info("Starting Object Detection API Server")
    logging.info(f"Saved frames dir: {SAVED_FRAMES_DIR.resolve()}")
    logging.info(f"Model loaded: {'yes' if model else 'no'}, device: {device}")
    logging.info(f"Default camera index: {camera_index}")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

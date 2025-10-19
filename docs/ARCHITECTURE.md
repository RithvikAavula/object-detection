# 📐 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BROWSER (localhost:3000)                          │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                        React Application                              │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │                       App.js (Main)                             │ │ │
│  │  │  • Loading Animation (2s)                                       │ │ │
│  │  │  • Particle Background                                          │ │ │
│  │  │  • Route to Dashboard                                           │ │ │
│  │  └────────────────────┬────────────────────────────────────────────┘ │ │
│  │                       │                                               │ │
│  │  ┌────────────────────▼───────────────────────────────────────────┐ │ │
│  │  │                   Dashboard.js                                  │ │ │
│  │  │  • State Management (isDetecting, metrics, frames)              │ │ │
│  │  │  • API Integration (Axios)                                      │ │ │
│  │  │  • Polling (metrics: 1s, frames: 5s)                            │ │ │
│  │  └─┬──────────────┬──────────────┬──────────────┬────────────────┘ │ │
│  │    │              │              │              │                   │ │
│  │  ┌─▼──────────┐ ┌─▼──────────┐ ┌─▼──────────┐ ┌─▼──────────────┐  │ │
│  │  │ LiveFeed   │ │ Controls   │ │ Metrics    │ │ SavedFrames    │  │ │
│  │  │            │ │            │ │            │ │                │  │ │
│  │  │ • Video    │ │ • Start/   │ │ • 5 Cards  │ │ • Grid         │  │ │
│  │  │   Stream   │ │   Stop     │ │ • FPS      │ │   Gallery      │  │ │
│  │  │ • Boxes    │ │ • Save     │ │   Chart    │ │ • Lightbox     │  │ │
│  │  │ • Labels   │ │ • Slider   │ │ • Objects  │ │ • Actions      │  │ │
│  │  │ • Status   │ │ • Buttons  │ │   List     │ │ • Download     │  │ │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────────┘  │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                          Particles.js                                 │ │
│  │  • Canvas Animation                                                   │ │
│  │  • Floating Particles                                                 │ │
│  │  • Connection Lines                                                   │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               │ HTTP Requests (Axios)
                               │ • GET /api/metrics (1s polling)
                               │ • GET /api/saved-frames (5s polling)
                               │ • POST /api/start
                               │ • POST /api/stop
                               │ • POST /api/save-frame
                               │ • POST /api/confidence
                               │ • DELETE /api/delete-frame/<name>
                               │
                               │ Video Stream
                               │ • GET /api/video-feed (MJPEG)
                               │
┌──────────────────────────────▼──────────────────────────────────────────────┐
│                        FLASK SERVER (localhost:5000)                        │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                           app.py                                      │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │                      API Endpoints                              │ │ │
│  │  │                                                                 │ │ │
│  │  │  Detection Control:                                             │ │ │
│  │  │  • POST /api/start      → start_detection()                     │ │ │
│  │  │  • POST /api/stop       → stop_detection()                      │ │ │
│  │  │  • GET  /api/status     → get_status()                          │ │ │
│  │  │                                                                 │ │ │
│  │  │  Metrics & Data:                                                │ │ │
│  │  │  • GET  /api/metrics    → get_metrics()                         │ │ │
│  │  │  • POST /api/confidence → set_confidence()                      │ │ │
│  │  │  • GET  /api/stats      → get_stats()                           │ │ │
│  │  │                                                                 │ │ │
│  │  │  Frame Management:                                              │ │ │
│  │  │  • POST /api/save-frame   → save_frame()                        │ │ │
│  │  │  • GET  /api/saved-frames → get_saved_frames()                  │ │ │
│  │  │  • DELETE /api/delete-frame/<name> → delete_frame()             │ │ │
│  │  │                                                                 │ │ │
│  │  │  Video Stream:                                                  │ │ │
│  │  │  • GET /api/video-feed  → video_feed()                          │ │ │
│  │  │                                                                 │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │                   Global State                                  │ │ │
│  │  │                                                                 │ │ │
│  │  │  detection_active = False                                       │ │ │
│  │  │  camera = None                                                  │ │ │
│  │  │  model = YOLO('yolov8m.pt')                                     │ │ │
│  │  │  current_metrics = { fps, confidence, object_count, ... }       │ │ │
│  │  │  current_frame = None                                           │ │ │
│  │  │  frame_lock = threading.Lock()                                  │ │ │
│  │  │  detection_thread = None                                        │ │ │
│  │  │                                                                 │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │              Detection Thread (Background)                      │ │ │
│  │  │                                                                 │ │ │
│  │  │  detection_loop():                                              │ │ │
│  │  │    while detection_active:                                      │ │ │
│  │  │      1. Read frame from camera                                  │ │ │
│  │  │      2. Run YOLO detection                                      │ │ │
│  │  │      3. Draw bounding boxes & labels                            │ │ │
│  │  │      4. Calculate FPS                                           │ │ │
│  │  │      5. Update metrics                                          │ │ │
│  │  │      6. Store frame (with lock)                                 │ │ │
│  │  │                                                                 │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  │                       │                                               │ │
│  └───────────────────────┼───────────────────────────────────────────────┘ │
│                          │                                                 │
└──────────────────────────┼─────────────────────────────────────────────────┘
                           │
                           │ Camera Access (OpenCV)
                           │ • cv2.VideoCapture(0)
                           │ • 640x480 resolution
                           │ • Buffer size: 1
                           │
┌──────────────────────────▼─────────────────────────────────────────────────┐
│                           YOLO Detection Engine                             │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                     Ultralytics YOLOv8                                │ │
│  │                                                                       │ │
│  │  model.predict():                                                     │ │
│  │    • Input: BGR frame (640x480)                                       │ │
│  │    • Confidence: 0.15 (adjustable)                                    │ │
│  │    • IoU: 0.40                                                        │ │
│  │    • Max Detections: 500                                              │ │
│  │    • Augmentation: OFF (speed)                                        │ │
│  │    • Classes: 80 COCO classes                                         │ │
│  │                                                                       │ │
│  │  Output:                                                              │ │
│  │    • Bounding boxes [x1, y1, x2, y2]                                  │ │
│  │    • Class IDs [0-79]                                                 │ │
│  │    • Confidence scores [0.0-1.0]                                      │ │
│  │    • Class names ['person', 'bottle', ...]                            │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         Model Files                                   │ │
│  │                                                                       │ │
│  │  • yolov8m.pt    - Primary model (25 MB)                              │ │
│  │  • yolov5su.pt   - Fallback model (20 MB)                             │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                           │
                           │ Camera Feed
                           │ • 30 FPS capture
                           │ • BGR format
                           │ • 640x480 pixels
                           │
┌──────────────────────────▼─────────────────────────────────────────────────┐
│                              WEBCAM                                         │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                     Physical Camera Device                            │ │
│  │                                                                       │ │
│  │  • USB Webcam or Built-in Camera                                      │ │
│  │  • Resolution: 640x480 recommended                                    │ │
│  │  • FPS: 30 recommended                                                │ │
│  │  • Auto-focus: Enabled                                                │ │
│  │  • Auto-exposure: Enabled                                             │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           FILE SYSTEM                                       │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                      saved_frames/                                    │ │
│  │                                                                       │ │
│  │  detection_20251019_143052_frame123.jpg                               │ │
│  │  detection_20251019_143055_frame145.jpg                               │ │
│  │  detection_20251019_143058_frame167.jpg                               │ │
│  │  ...                                                                  │ │
│  │                                                                       │ │
│  │  • Auto-created folder                                                │ │
│  │  • Timestamped filenames                                              │ │
│  │  • JPEG format                                                        │ │
│  │  • Quality: 95%                                                       │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘


════════════════════════════════════════════════════════════════════════════
                            DATA FLOW
════════════════════════════════════════════════════════════════════════════

1. USER ACTION (Browser)
   User clicks "Start Detection"
   ↓
2. FRONTEND (React)
   Dashboard.handleStart() → axios.post('/api/start')
   ↓
3. BACKEND (Flask)
   POST /api/start → start_detection()
   ↓
4. THREAD START
   detection_thread = Thread(target=detection_loop)
   detection_thread.start()
   ↓
5. CAMERA INIT
   camera = cv2.VideoCapture(0)
   camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   ↓
6. DETECTION LOOP (Background Thread)
   while detection_active:
     • Read frame from camera
     • Run YOLO detection
     • Draw boxes & labels
     • Calculate FPS
     • Update metrics
     • Store frame (thread-safe)
   ↓
7. VIDEO STREAMING
   GET /api/video-feed → video_feed()
   • Read current_frame (with lock)
   • Encode to JPEG
   • Stream as multipart/x-mixed-replace
   ↓
8. FRONTEND DISPLAY
   <img src="/api/video-feed" />
   • Browser displays MJPEG stream
   • ~30 FPS
   • Auto-updates
   ↓
9. METRICS POLLING
   Every 1 second:
     • GET /api/metrics
     • Update dashboard state
     • Re-render components
     • Animate changes
   ↓
10. USER SAVES FRAME
    User clicks "Save Current Frame"
    ↓
11. SAVE REQUEST
    POST /api/save-frame
    • Copy current_frame
    • Generate filename with timestamp
    • Save to saved_frames/
    • Increment saved_count
    ↓
12. GALLERY UPDATE
    Every 5 seconds:
      • GET /api/saved-frames
      • Update gallery
      • Show new frames
   ↓
13. USER STOPS
    User clicks "Stop Detection"
    ↓
14. STOP REQUEST
    POST /api/stop
    • detection_active = False
    • Thread exits loop
    • camera.release()
    • Clean shutdown


════════════════════════════════════════════════════════════════════════════
                         COMMUNICATION PROTOCOLS
════════════════════════════════════════════════════════════════════════════

Frontend → Backend:
  • Protocol: HTTP/1.1
  • Format: JSON (requests & responses)
  • CORS: Enabled (all origins in dev)
  • Polling: 1s (metrics), 5s (frames)
  • Streaming: MJPEG (video feed)

Backend → YOLO:
  • Protocol: Python function calls
  • Format: NumPy arrays (BGR)
  • Output: Ultralytics Results objects

Backend → Camera:
  • Protocol: OpenCV API
  • Format: BGR frames
  • Resolution: 640x480
  • FPS: 30

Backend → Filesystem:
  • Protocol: File I/O
  • Format: JPEG images
  • Location: saved_frames/
  • Naming: timestamp-based


════════════════════════════════════════════════════════════════════════════
                         THREADING MODEL
════════════════════════════════════════════════════════════════════════════

Main Thread (Flask):
  • Handle HTTP requests
  • Serve static files
  • Return JSON responses
  • Stream video frames

Detection Thread:
  • Capture camera frames
  • Run YOLO detection
  • Process results
  • Update metrics
  • Store current frame

Synchronization:
  • frame_lock (threading.Lock)
  • Protects current_frame
  • Used by detection thread (write)
  • Used by video stream (read)

Thread Safety:
  • Global variables protected
  • Atomic operations
  • No race conditions
  • Clean shutdown


════════════════════════════════════════════════════════════════════════════
                         PERFORMANCE CHARACTERISTICS
════════════════════════════════════════════════════════════════════════════

Latency:
  • Camera to Detection: ~10ms
  • Detection Processing: ~30ms
  • Frame to Browser: ~10ms
  • Total: ~50ms (20 FPS)

Throughput:
  • Video Stream: ~2 Mbps
  • API Requests: ~10 req/s
  • Metrics Updates: 1 Hz
  • Frame Saves: On-demand

Resource Usage:
  • CPU: 30-50% (single core)
  • RAM: ~500 MB
  • Disk: ~1 MB/frame saved
  • Network: ~2 Mbps (local)

Scalability:
  • Single camera per instance
  • Multiple browser clients OK
  • CPU-bound (detection)
  • Can run on modest hardware


════════════════════════════════════════════════════════════════════════════

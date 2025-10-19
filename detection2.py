import cv2
from ultralytics import YOLO
import time
import os
from collections import defaultdict
from datetime import datetime

# Create folder for saved frames
SAVE_FOLDER = "saved_frames"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
    print(f"Created folder: {SAVE_FOLDER}")

# Load the YOLO model - using YOLOv8 for better accuracy
print("Loading YOLO model...")
try:
    # Try YOLOv8 medium model for better detection accuracy
    model = YOLO("yolov8m.pt")
    print("✓ Using YOLOv8 Medium - Better accuracy")
except Exception as e:
    try:
        # Fallback to YOLOv5 if available
        model = YOLO("yolov5su.pt")
        print("✓ Using YOLOv5 - Standard detection")
    except Exception as e2:
        print(f"✗ Error loading model: {e2}")
        print("Please ensure model files are available or connected to internet for download")
        exit(1)

# Configure model for maximum detection sensitivity
model.conf = 0.15  # Lower confidence threshold to detect more objects
model.iou = 0.40   # Lower IoU for better detection of similar objects
model.max_det = 500  # Increased maximum detections per image

# Open webcam with enhanced settings for better detection
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Standard resolution for smooth performance
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce latency
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Enable autofocus for clarity
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # Auto exposure for better lighting

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Tracking variables
fps_time = time.time()
fps_counter = 0
fps_display = 0
frame_count = 0
saved_count = 0
total_detections = 0
object_counts = defaultdict(int)

print("\n" + "="*50)
print("Enhanced Object Detection Started!")
print("="*50)
print("Controls:")
print("  'q' - Quit")
print("  's' - Save frame to 'saved_frames' folder")
print("  '+' - Increase confidence (fewer detections)")
print("  '-' - Decrease confidence (more detections)")
print(f"\nCurrent Settings:")
print(f"  Confidence threshold: {model.conf:.2f}")
print(f"  Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
print("\nDetectable Objects:")
print("  80 COCO classes: person, bottle, cup, bowl, chair,")
print("  laptop, mouse, keyboard, cell phone, book, clock,")
print("  scissors, toothbrush, and many more!")
print("\nNote: Hold objects steady for 1-2 seconds for detection")
print("="*50 + "\n")

while True:
    try:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Warning: Failed to grab frame. Retrying...")
            time.sleep(0.1)
            continue

        frame_count += 1
        
        # Run YOLO detection with enhanced settings
        results = model(
            frame, 
            verbose=False,
            augment=False,  # Disabled for smoother performance
            agnostic_nms=False  # Class-specific NMS
        )

        # Get the annotated frame
        annotated_frame = results[0].plot()
        
        # Extract detection information
        boxes = results[0].boxes
        current_detections = defaultdict(int)
        total_current = 0
        
        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                cls_id = int(box.cls[0])
                class_name = results[0].names[cls_id]
                current_detections[class_name] += 1
                object_counts[class_name] += 1
                total_current += 1
        
        total_detections += total_current
        
        # Calculate FPS
        fps_counter += 1
        if time.time() - fps_time > 1:
            fps_display = fps_counter
            fps_counter = 0
            fps_time = time.time()
        
        # Create info panel with semi-transparent background
        panel_height = 200
        panel_width = 280
        overlay = annotated_frame.copy()
        cv2.rectangle(overlay, (5, 5), (panel_width, panel_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, annotated_frame, 0.4, 0, annotated_frame)
        
        # Add metrics display
        y_pos = 30
        line_height = 28
        
        # FPS
        cv2.putText(annotated_frame, f"FPS: {fps_display}", (15, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        y_pos += line_height
        
        # Confidence threshold display
        cv2.putText(annotated_frame, f"Conf: {model.conf:.2f}", (15, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 255), 2)
        y_pos += line_height
        
        # Total objects in current frame
        cv2.putText(annotated_frame, f"Objects: {total_current}", (15, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        y_pos += line_height
        
        # Frame count
        cv2.putText(annotated_frame, f"Frames: {frame_count}", (15, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 100), 2)
        y_pos += line_height
        
        # Saved frames count
        cv2.putText(annotated_frame, f"Saved: {saved_count}", (15, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 255), 2)
        y_pos += line_height
        
        # Show detected objects in current frame
        if current_detections:
            y_pos += 5
            cv2.putText(annotated_frame, "Detected:", (15, y_pos), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            y_pos += 20
            
            for obj_name, count in sorted(current_detections.items())[:4]:  # Top 4
                cv2.putText(annotated_frame, f"{obj_name}: {count}", (20, y_pos), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 255, 150), 1)
                y_pos += 18
        else:
            y_pos += 5
            cv2.putText(annotated_frame, "No objects", (15, y_pos), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
            y_pos += 20
            cv2.putText(annotated_frame, "Hold object", (15, y_pos), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)
            y_pos += 18
            cv2.putText(annotated_frame, "in frame", (15, y_pos), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)
        
        # Show the frame
        cv2.imshow("Object Detection - Press 'q' to quit, 's' to save", annotated_frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            # Quit
            print("\nExiting...")
            break
        elif key == ord('s'):
            # Save current frame with timestamp
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"detection_{timestamp}_frame{frame_count}.jpg"
                filepath = os.path.join(SAVE_FOLDER, filename)
                cv2.imwrite(filepath, annotated_frame)
                saved_count += 1
                print(f"✓ Frame saved: {filepath}")
            except Exception as e:
                print(f"✗ Error saving frame: {e}")
        elif key == ord('+') or key == ord('='):
            # Increase confidence threshold (fewer detections, more accurate)
            model.conf = min(0.95, model.conf + 0.05)
            print(f"✓ Confidence increased to {model.conf:.2f} (fewer detections)")
        elif key == ord('-') or key == ord('_'):
            # Decrease confidence threshold (more detections, less accurate)
            model.conf = max(0.05, model.conf - 0.05)
            print(f"✓ Confidence decreased to {model.conf:.2f} (more detections)")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        break
    except Exception as e:
        print(f"⚠ Error in frame {frame_count}: {e}")
        continue

# Print session summary
print("\n" + "="*50)
print("Detection Session Summary")
print("="*50)
print(f"Total frames processed: {frame_count}")
print(f"Frames saved: {saved_count}")
if frame_count > 0:
    avg_fps = frame_count / max(1, time.time() - fps_time + frame_count/max(1, fps_display))
    print(f"Average FPS: {avg_fps:.1f}")
print(f"\nTotal detections: {total_detections}")
if object_counts:
    print(f"\nTop detected objects:")
    for obj_name, count in sorted(object_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {obj_name}: {count}")
else:
    print("\nNo objects were detected during this session")
print(f"\nSaved frames location: ./{SAVE_FOLDER}/")
print("="*50)

# Release resources
try:
    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Resources released successfully")
except Exception as e:
    print(f"\n⚠ Warning during cleanup: {e}")

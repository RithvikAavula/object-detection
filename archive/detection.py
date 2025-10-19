import cv2
import os
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolov5su.pt")

# Folder containing multiple images
image_folder = "E:/object detection"  # Change to your image folder path

# Supported image extensions
extensions = [".jpg", ".jpeg", ".png"]

# Loop through each image in the folder
for filename in os.listdir(image_folder):
    if any(filename.lower().endswith(ext) for ext in extensions):
        image_path = os.path.join(image_folder, filename)
        print(f"\nProcessing: {image_path}")

        # Read the image
        image = cv2.imread(image_path)

        # Run detection
        results = model(image)

        # Display the result
        annotated_frame = results[0].plot()
        cv2.imshow("YOLO Detection", annotated_frame)

        # Wait for key press to move to next image
        cv2.waitKey(0)

cv2.destroyAllWindows()

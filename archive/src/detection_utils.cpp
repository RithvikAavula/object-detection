/**
 * Utility functions for object detection optimization
 */

#include <opencv2/opencv.hpp>
#include <vector>
#include <algorithm>

class DetectionUtils {
public:
    /**
     * Fast Non-Maximum Suppression (NMS)
     * Optimized implementation for removing overlapping boxes
     */
    static std::vector<int> fastNMS(const std::vector<cv::Rect>& boxes, 
                                    const std::vector<float>& scores,
                                    float iouThreshold = 0.45) {
        std::vector<int> indices(boxes.size());
        std::iota(indices.begin(), indices.end(), 0);
        
        // Sort by scores in descending order
        std::sort(indices.begin(), indices.end(), [&scores](int i1, int i2) {
            return scores[i1] > scores[i2];
        });
        
        std::vector<bool> suppressed(boxes.size(), false);
        std::vector<int> keep;
        
        for (size_t i = 0; i < indices.size(); ++i) {
            int idx = indices[i];
            if (suppressed[idx]) continue;
            
            keep.push_back(idx);
            
            for (size_t j = i + 1; j < indices.size(); ++j) {
                int idx2 = indices[j];
                if (suppressed[idx2]) continue;
                
                float iou = computeIoU(boxes[idx], boxes[idx2]);
                if (iou > iouThreshold) {
                    suppressed[idx2] = true;
                }
            }
        }
        
        return keep;
    }
    
    /**
     * Compute Intersection over Union (IoU) between two boxes
     */
    static float computeIoU(const cv::Rect& box1, const cv::Rect& box2) {
        int x1 = std::max(box1.x, box2.x);
        int y1 = std::max(box1.y, box2.y);
        int x2 = std::min(box1.x + box1.width, box2.x + box2.width);
        int y2 = std::min(box1.y + box1.height, box2.y + box2.height);
        
        int intersection = std::max(0, x2 - x1) * std::max(0, y2 - y1);
        int union_area = box1.area() + box2.area() - intersection;
        
        return union_area > 0 ? static_cast<float>(intersection) / union_area : 0.0f;
    }
    
    /**
     * Optimize bounding box visualization
     * Draw boxes with optimized OpenCV calls
     */
    static void drawOptimizedBoxes(cv::Mat& image, 
                                   const std::vector<cv::Rect>& boxes,
                                   const std::vector<std::string>& labels,
                                   const std::vector<float>& confidences,
                                   const cv::Scalar& color = cv::Scalar(0, 255, 0)) {
        for (size_t i = 0; i < boxes.size(); ++i) {
            // Draw rectangle
            cv::rectangle(image, boxes[i], color, 2);
            
            // Prepare label text
            std::string label = labels[i] + ": " + 
                               std::to_string(static_cast<int>(confidences[i] * 100)) + "%";
            
            // Get text size for background
            int baseline;
            cv::Size textSize = cv::getTextSize(label, cv::FONT_HERSHEY_SIMPLEX, 
                                                0.5, 1, &baseline);
            
            // Draw label background
            cv::Point textOrg(boxes[i].x, boxes[i].y - 5);
            cv::rectangle(image, 
                         textOrg + cv::Point(0, baseline),
                         textOrg + cv::Point(textSize.width, -textSize.height),
                         color, cv::FILLED);
            
            // Draw label text
            cv::putText(image, label, textOrg, cv::FONT_HERSHEY_SIMPLEX, 
                       0.5, cv::Scalar(0, 0, 0), 1);
        }
    }
    
    /**
     * Frame rate stabilizer - smooth out FPS fluctuations
     */
    static float stabilizeFPS(float currentFPS, float previousFPS, float alpha = 0.1f) {
        return alpha * currentFPS + (1.0f - alpha) * previousFPS;
    }
};

/**
 * Python bindings for C++ acceleration module
 * Uses pybind11 for seamless Python integration
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <opencv2/opencv.hpp>
#include "image_processor.cpp"
#include "detection_utils.cpp"

namespace py = pybind11;

// Convert numpy array to cv::Mat
cv::Mat numpy_to_mat(py::array_t<uint8_t> input) {
    py::buffer_info buf = input.request();
    
    if (buf.ndim != 3)
        throw std::runtime_error("Input must be a 3D array");
    
    return cv::Mat(buf.shape[0], buf.shape[1], CV_8UC3, (uint8_t*)buf.ptr);
}

// Convert cv::Mat to numpy array
py::array_t<uint8_t> mat_to_numpy(cv::Mat& mat) {
    return py::array_t<uint8_t>(
        {mat.rows, mat.cols, mat.channels()},
        {mat.step[0], mat.step[1], sizeof(uint8_t)},
        mat.data
    );
}

// Wrapper class for Python
class PyImageProcessor {
public:
    PyImageProcessor() : processor() {}
    
    py::array_t<uint8_t> process_frame(py::array_t<uint8_t> input) {
        cv::Mat input_mat = numpy_to_mat(input);
        cv::Mat output_mat = processor.processFrame(input_mat);
        return mat_to_numpy(output_mat);
    }
    
    std::vector<py::array_t<uint8_t>> process_batch(std::vector<py::array_t<uint8_t>> inputs) {
        std::vector<cv::Mat> input_mats;
        for (auto& input : inputs) {
            input_mats.push_back(numpy_to_mat(input));
        }
        
        std::vector<cv::Mat> output_mats = processor.processBatch(input_mats);
        
        std::vector<py::array_t<uint8_t>> outputs;
        for (auto& mat : output_mats) {
            outputs.push_back(mat_to_numpy(mat));
        }
        
        return outputs;
    }

private:
    ImageProcessor processor;
};

PYBIND11_MODULE(detection_accelerator, m) {
    m.doc() = "C++ Acceleration module for object detection";
    
    py::class_<PyImageProcessor>(m, "ImageProcessor")
        .def(py::init<>())
        .def("process_frame", &PyImageProcessor::process_frame,
             "Process a single frame with optimized C++ code",
             py::arg("frame"))
        .def("process_batch", &PyImageProcessor::process_batch,
             "Process multiple frames in parallel",
             py::arg("frames"));
    
    py::class_<DetectionUtils>(m, "DetectionUtils")
        .def_static("fast_nms", [](py::list boxes, py::list scores, float threshold) {
            std::vector<cv::Rect> box_vec;
            std::vector<float> score_vec;
            
            for (auto item : boxes) {
                auto box = item.cast<py::list>();
                box_vec.push_back(cv::Rect(
                    box[0].cast<int>(), box[1].cast<int>(),
                    box[2].cast<int>(), box[3].cast<int>()
                ));
            }
            
            for (auto item : scores) {
                score_vec.push_back(item.cast<float>());
            }
            
            return DetectionUtils::fastNMS(box_vec, score_vec, threshold);
        }, "Fast Non-Maximum Suppression",
        py::arg("boxes"), py::arg("scores"), py::arg("threshold") = 0.45f)
        
        .def_static("compute_iou", [](py::list box1, py::list box2) {
            cv::Rect r1(box1[0].cast<int>(), box1[1].cast<int>(),
                       box1[2].cast<int>(), box1[3].cast<int>());
            cv::Rect r2(box2[0].cast<int>(), box2[1].cast<int>(),
                       box2[2].cast<int>(), box2[3].cast<int>());
            return DetectionUtils::computeIoU(r1, r2);
        }, "Compute IoU between two boxes",
        py::arg("box1"), py::arg("box2"))
        
        .def_static("stabilize_fps", &DetectionUtils::stabilizeFPS,
                   "Stabilize FPS measurements",
                   py::arg("current_fps"), py::arg("previous_fps"), 
                   py::arg("alpha") = 0.1f);
    
    #ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
    #else
    m.attr("__version__") = "1.0.0";
    #endif
}

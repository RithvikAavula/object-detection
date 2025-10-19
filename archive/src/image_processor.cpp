/**
 * High-Performance Image Preprocessing for Object Detection
 * Optimized C++ implementation for faster frame processing
 */

#include <opencv2/opencv.hpp>
#include <opencv2/core/cuda.hpp>
#include <vector>
#include <thread>

#ifdef USE_CUDA
#include <opencv2/cudaimgproc.hpp>
#include <opencv2/cudafilters.hpp>
#endif

class ImageProcessor {
public:
    ImageProcessor() {
        #ifdef USE_CUDA
        try {
            if (cv::cuda::getCudaEnabledDeviceCount() > 0) {
                useCUDA = true;
                cv::cuda::setDevice(0);
                std::cout << "CUDA acceleration enabled for image processing" << std::endl;
            }
        } catch(...) {
            useCUDA = false;
        }
        #endif
    }

    /**
     * Fast CLAHE (Contrast Limited Adaptive Histogram Equalization)
     * Optimized for real-time processing
     */
    cv::Mat applyCLAHE(const cv::Mat& input, double clipLimit = 2.0, int tileSize = 8) {
        cv::Mat lab, result;
        cv::cvtColor(input, lab, cv::COLOR_BGR2LAB);
        
        std::vector<cv::Mat> lab_planes;
        cv::split(lab, lab_planes);
        
        #ifdef USE_CUDA
        if (useCUDA) {
            cv::cuda::GpuMat gpu_l, gpu_result;
            gpu_l.upload(lab_planes[0]);
            
            cv::Ptr<cv::cuda::CLAHE> clahe = cv::cuda::createCLAHE(clipLimit, cv::Size(tileSize, tileSize));
            clahe->apply(gpu_l, gpu_result);
            
            gpu_result.download(lab_planes[0]);
        } else
        #endif
        {
            cv::Ptr<cv::CLAHE> clahe = cv::createCLAHE(clipLimit, cv::Size(tileSize, tileSize));
            clahe->apply(lab_planes[0], lab_planes[0]);
        }
        
        cv::merge(lab_planes, lab);
        cv::cvtColor(lab, result, cv::COLOR_LAB2BGR);
        
        return result;
    }

    /**
     * Fast sharpening using optimized convolution
     */
    cv::Mat sharpenImage(const cv::Mat& input, float amount = 0.3) {
        cv::Mat kernel = (cv::Mat_<float>(3, 3) << 
            -1, -1, -1,
            -1,  9, -1,
            -1, -1, -1);
        
        cv::Mat sharpened;
        
        #ifdef USE_CUDA
        if (useCUDA) {
            cv::cuda::GpuMat gpu_input, gpu_sharpened;
            gpu_input.upload(input);
            
            cv::Ptr<cv::cuda::Filter> filter = cv::cuda::createLinearFilter(
                gpu_input.type(), -1, kernel);
            filter->apply(gpu_input, gpu_sharpened);
            
            gpu_sharpened.download(sharpened);
        } else
        #endif
        {
            cv::filter2D(input, sharpened, -1, kernel);
        }
        
        cv::Mat result;
        cv::addWeighted(input, 1.0 - amount, sharpened, amount, 0, result);
        
        return result;
    }

    /**
     * Fast noise reduction with edge preservation
     */
    cv::Mat denoise(const cv::Mat& input) {
        cv::Mat result;
        
        #ifdef USE_CUDA
        if (useCUDA) {
            cv::cuda::GpuMat gpu_input, gpu_result;
            gpu_input.upload(input);
            
            // Fast bilateral filter on GPU
            cv::cuda::bilateralFilter(gpu_input, gpu_result, 5, 50, 50);
            gpu_result.download(result);
        } else
        #endif
        {
            // CPU fallback: fast NLMeans
            cv::fastNlMeansDenoisingColored(input, result, 6, 6, 7, 21);
        }
        
        return result;
    }

    /**
     * Complete preprocessing pipeline - optimized
     */
    cv::Mat processFrame(const cv::Mat& input) {
        auto start = std::chrono::high_resolution_clock::now();
        
        // Step 1: CLAHE for better contrast
        cv::Mat enhanced = applyCLAHE(input, 2.0, 8);
        
        // Step 2: Sharpening for edge clarity
        cv::Mat sharpened = sharpenImage(enhanced, 0.3);
        
        // Step 3: Denoise while preserving edges
        cv::Mat denoised = denoise(sharpened);
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        // Optional: print processing time for benchmarking
        // std::cout << "Frame preprocessing: " << duration.count() << "ms" << std::endl;
        
        return denoised;
    }

    /**
     * Batch processing for multiple frames (multi-threaded)
     */
    std::vector<cv::Mat> processBatch(const std::vector<cv::Mat>& frames) {
        std::vector<cv::Mat> results(frames.size());
        std::vector<std::thread> threads;
        
        unsigned int numThreads = std::thread::hardware_concurrency();
        unsigned int framesPerThread = frames.size() / numThreads + 1;
        
        for (unsigned int t = 0; t < numThreads; ++t) {
            threads.push_back(std::thread([&, t]() {
                unsigned int start = t * framesPerThread;
                unsigned int end = std::min(start + framesPerThread, 
                                           static_cast<unsigned int>(frames.size()));
                
                for (unsigned int i = start; i < end; ++i) {
                    results[i] = processFrame(frames[i]);
                }
            }));
        }
        
        for (auto& thread : threads) {
            thread.join();
        }
        
        return results;
    }

private:
    bool useCUDA = false;
};

// Export C interface for easy integration
extern "C" {
    ImageProcessor* ImageProcessor_new() {
        return new ImageProcessor();
    }
    
    void ImageProcessor_delete(ImageProcessor* processor) {
        delete processor;
    }
    
    void ImageProcessor_process(ImageProcessor* processor, 
                               unsigned char* input_data, int width, int height,
                               unsigned char* output_data) {
        cv::Mat input(height, width, CV_8UC3, input_data);
        cv::Mat output = processor->processFrame(input);
        std::memcpy(output_data, output.data, width * height * 3);
    }
}

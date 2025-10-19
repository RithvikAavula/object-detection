cmake_minimum_required(VERSION 3.15)
project(ObjectDetectionAccelerator VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find OpenCV
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# Find Python
find_package(Python3 COMPONENTS Development NumPy REQUIRED)
include_directories(${Python3_INCLUDE_DIRS})

# Find pybind11 for Python bindings
find_package(pybind11 CONFIG)

# Enable CUDA if available for GPU acceleration
include(CheckLanguage)
check_language(CUDA)
if(CMAKE_CUDA_COMPILER)
    enable_language(CUDA)
    set(CMAKE_CUDA_STANDARD 17)
    add_definitions(-DUSE_CUDA)
    message(STATUS "CUDA support enabled")
endif()

# Optimization flags
if(MSVC)
    add_compile_options(/O2 /arch:AVX2 /fp:fast)
else()
    add_compile_options(-O3 -march=native -ffast-math)
endif()

# Source files for image preprocessing acceleration
set(SOURCES
    src/image_processor.cpp
    src/detection_utils.cpp
)

# Create shared library for Python integration
if(pybind11_FOUND)
    pybind11_add_module(detection_accelerator ${SOURCES} src/python_bindings.cpp)
    target_link_libraries(detection_accelerator PRIVATE ${OpenCV_LIBS})
    
    if(CMAKE_CUDA_COMPILER)
        target_link_libraries(detection_accelerator PRIVATE cuda cudart)
    endif()
    
    message(STATUS "Building Python module with acceleration support")
else()
    # Fallback: build as standalone library
    add_library(detection_accelerator SHARED ${SOURCES})
    target_link_libraries(detection_accelerator ${OpenCV_LIBS})
    message(STATUS "Building as standalone library (pybind11 not found)")
endif()

# Installation
install(TARGETS detection_accelerator
        LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
        RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/bin)

message(STATUS "")
message(STATUS "Configuration Summary:")
message(STATUS "  OpenCV Version: ${OpenCV_VERSION}")
message(STATUS "  Python Version: ${Python3_VERSION}")
message(STATUS "  CUDA Support: ${CMAKE_CUDA_COMPILER}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "")

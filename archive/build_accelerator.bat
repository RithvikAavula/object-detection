@echo off
REM Build script for C++ acceleration module on Windows
REM Requires: CMake, Visual Studio, OpenCV, Python development headers

echo ====================================================
echo   Building Object Detection C++ Accelerator
echo ====================================================
echo.

REM Create build directory
if not exist "build" mkdir build
cd build

REM Configure with CMake
echo Configuring with CMake...
cmake .. -G "Visual Studio 17 2022" -A x64 ^
    -DCMAKE_BUILD_TYPE=Release ^
    -DOpenCV_DIR="C:/opencv/build" ^
    -Dpybind11_DIR="C:/pybind11/share/cmake/pybind11"

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: CMake configuration failed!
    echo Please ensure OpenCV and pybind11 are installed.
    pause
    exit /b 1
)

echo.
echo Building project...
cmake --build . --config Release

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ====================================================
echo   Build completed successfully!
echo ====================================================
echo.
echo The acceleration module is in: build\Release\
echo Copy detection_accelerator.pyd to the project directory.
echo.

cd ..
pause

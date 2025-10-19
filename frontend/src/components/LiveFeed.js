import React, { useRef, useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { FaVideo, FaVideoSlash } from 'react-icons/fa';
import './LiveFeed.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';
const USE_BROWSER_CAMERA = true; // Toggle: true for WebRTC, false for server camera

function LiveFeed({ isDetecting }) {
  const imgRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const [cameraError, setCameraError] = useState(null);
  const [processedFrame, setProcessedFrame] = useState(null);
  const [cameraReady, setCameraReady] = useState(false);

  // Request camera access from browser
  useEffect(() => {
    if (USE_BROWSER_CAMERA && isDetecting) {
      startBrowserCamera();
    } else if (!isDetecting && streamRef.current) {
      stopBrowserCamera();
    }

    return () => {
      stopBrowserCamera();
    };
  }, [isDetecting]);

  // Send frames to backend for processing
  useEffect(() => {
    if (USE_BROWSER_CAMERA && isDetecting && cameraReady && videoRef.current) {
      console.log('Starting frame capture interval...');
      const interval = setInterval(() => {
        captureAndSendFrame();
      }, 100); // Send 10 frames per second

      return () => {
        console.log('Stopping frame capture interval');
        clearInterval(interval);
      };
    }
  }, [isDetecting, cameraReady]);

  const startBrowserCamera = async () => {
    try {
      console.log('Requesting camera access...');
      setCameraReady(false);
      
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        }
      });
      
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        
        // Wait for video to actually start playing
        videoRef.current.onloadedmetadata = () => {
          videoRef.current.play().then(() => {
            console.log('✅ Camera access granted and video playing!');
            setCameraReady(true);
            setCameraError(null);
          }).catch(err => {
            console.error('Error playing video:', err);
            setCameraError(`Playback Error: ${err.message}`);
          });
        };
      }
    } catch (err) {
      console.error('Camera access denied:', err);
      setCameraError(`Camera Error: ${err.message}`);
      setCameraReady(false);
    }
  };

  const stopBrowserCamera = () => {
    setCameraReady(false);
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setProcessedFrame(null);
  };

  const captureAndSendFrame = async () => {
    if (!videoRef.current || !canvasRef.current) {
      console.warn('Video or canvas not ready');
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    // Check if video is actually playing
    if (video.readyState < 2) {
      console.warn('Video not ready, readyState:', video.readyState);
      return;
    }
    
    const ctx = canvas.getContext('2d');

    // Set canvas size to match video
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    if (canvas.width === 0 || canvas.height === 0) {
      console.warn('Invalid canvas dimensions');
      return;
    }

    // Draw current video frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to blob
    canvas.toBlob(async (blob) => {
      if (!blob) {
        console.warn('Failed to create blob');
        return;
      }

      try {
        // Send frame to backend
        const formData = new FormData();
        formData.append('frame', blob, 'frame.jpg');

        const response = await fetch(`${API_BASE}/api/process-frame`, {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          
          // Clean up old URL to prevent memory leaks
          if (processedFrame) {
            URL.revokeObjectURL(processedFrame);
          }
          
          setProcessedFrame(url);
          console.log('✅ Frame processed successfully');
        } else {
          console.error('Backend error:', response.status, response.statusText);
        }
      } catch (err) {
        console.error('Error sending frame:', err);
      }
    }, 'image/jpeg', 0.8);
  };

  // Fallback to original server camera method
  useEffect(() => {
    if (!USE_BROWSER_CAMERA && isDetecting && imgRef.current) {
      imgRef.current.decode()
        .then(() => {
          console.log('Video feed loaded');
        })
        .catch(err => {
          console.log('Preload error (normal):', err.message);
        });
    }
  }, [isDetecting]);

  return (
    <motion.div
      className="live-feed glass"
      whileHover={{ scale: 1.01 }}
      transition={{ duration: 0.2 }}
    >
      <div className="feed-header">
        <h2>
          {isDetecting ? <FaVideo className="icon-pulse" /> : <FaVideoSlash />}
          <span>Live Feed {USE_BROWSER_CAMERA && '(Browser Camera)'}</span>
        </h2>
        {isDetecting && (
          <motion.span
            className="recording-badge"
            animate={{
              opacity: [1, 0.5, 1],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
            }}
          >
            ● REC
          </motion.span>
        )}
      </div>

      <div className="feed-container">
        {cameraError && (
          <div className="camera-error">
            <p>{cameraError}</p>
            <small>Please allow camera access in your browser</small>
          </div>
        )}

        {isDetecting ? (
          USE_BROWSER_CAMERA ? (
            // WebRTC Mode: Show browser camera with processed overlay
            <div style={{ position: 'relative', width: '100%', height: '100%' }}>
              {/* Hidden canvas for frame processing */}
              <canvas ref={canvasRef} style={{ display: 'none' }} />
              
              {/* Display processed frame from backend OR live camera feed */}
              {processedFrame ? (
                // Show processed frame with detections
                <motion.img
                  src={processedFrame}
                  alt="Processed Detection Feed"
                  className="feed-video"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.3 }}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'contain'
                  }}
                />
              ) : cameraReady ? (
                // Show live camera feed while waiting for processed frames
                <video
                  ref={videoRef}
                  className="feed-video"
                  autoPlay
                  playsInline
                  muted
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'contain'
                  }}
                />
              ) : (
                // Show loading state
                <div className="feed-placeholder">
                  <motion.div
                    className="placeholder-icon"
                    animate={{
                      scale: [1, 1.1, 1],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                    }}
                  >
                    <FaVideo />
                  </motion.div>
                  <h3>Starting Camera...</h3>
                  <p>Please allow camera access</p>
                </div>
              )}
            </div>
          ) : (
            // Server Camera Mode: Original MJPEG stream
            <motion.img
              ref={imgRef}
              src={`${API_BASE}/api/video-feed?t=${Date.now()}`}
              alt="Live Detection Feed"
              className="feed-video"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              loading="eager"
              decoding="async"
              style={{
                imageRendering: 'auto',
                willChange: 'auto'
              }}
            />
          )
        ) : (
          <motion.div
            className="feed-placeholder"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <motion.div
              className="placeholder-icon"
              animate={{
                scale: [1, 1.1, 1],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
              }}
            >
              <FaVideoSlash />
            </motion.div>
            <h3>Detection Stopped</h3>
            <p>Click Start to begin object detection</p>
            {USE_BROWSER_CAMERA && (
              <small style={{ marginTop: '10px', opacity: 0.7 }}>
                📹 Will use your browser camera
              </small>
            )}
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

export default LiveFeed;

import React, { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaVideo, FaVideoSlash } from 'react-icons/fa';
import './LiveFeed.css';

function LiveFeed({ isDetecting }) {
  const imgRef = useRef(null);

  useEffect(() => {
    // Optimize image loading when detection starts
    if (isDetecting && imgRef.current) {
      // Preload image to reduce initial lag
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
          <span>Live Feed</span>
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
        {isDetecting ? (
          <motion.img
            ref={imgRef}
            src={`http://localhost:5000/api/video-feed?t=${Date.now()}`}
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
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

export default LiveFeed;

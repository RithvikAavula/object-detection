import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { FaPlay, FaPause, FaCamera, FaCog } from 'react-icons/fa';
import axios from 'axios';
import LiveFeed from './LiveFeed';
import MetricsPanel from './MetricsPanel';
import SavedFrames from './SavedFrames';
import Controls from './Controls';
import './Dashboard.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';
const API_URL = `${API_BASE}/api`;
const USE_BROWSER_CAMERA = true; // Must match LiveFeed.js setting

function Dashboard() {
  const [isDetecting, setIsDetecting] = useState(false);
  const [metrics, setMetrics] = useState({
    fps: 0,
    confidence: 0.15,
    object_count: 0,
    frames_processed: 0,
    saved_count: 0,
    detections: {}
  });
  const [savedFrames, setSavedFrames] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  // Fetch metrics periodically
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`${API_URL}/metrics`);
        setMetrics(response.data);
      } catch (error) {
        console.error('Error fetching metrics:', error);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  // Fetch saved frames
  const fetchSavedFrames = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/saved-frames`);
      setSavedFrames(response.data.frames);
    } catch (error) {
      console.error('Error fetching saved frames:', error);
    }
  }, []);

  useEffect(() => {
    fetchSavedFrames();
    const interval = setInterval(fetchSavedFrames, 5000);
    return () => clearInterval(interval);
  }, [fetchSavedFrames]);

  // Start detection
  const handleStart = async () => {
    setLoading(true);
    try {
      // If using browser camera, just toggle state (no backend camera needed)
      if (USE_BROWSER_CAMERA) {
        console.log('Using browser camera - no backend camera start needed');
        setIsDetecting(true);
      } else {
        // Server camera mode - call backend to start camera
        await axios.post(`${API_URL}/start`);
        setIsDetecting(true);
      }
    } catch (error) {
      console.error('Error starting detection:', error);
      
      // Show detailed error message if available
      if (error.response?.data?.error) {
        const errorMsg = error.response.data.error;
        const details = error.response.data.details;
        const suggestion = error.response.data.suggestion;
        
        let message = `Failed to start detection:\n\n${errorMsg}`;
        if (details) message += `\n\n${details}`;
        if (suggestion) message += `\n\n${suggestion}`;
        
        alert(message);
      } else {
        alert('Failed to start detection. Please check if the backend server is running.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Stop detection
  const handleStop = async () => {
    setLoading(true);
    try {
      // If using browser camera, just toggle state
      if (USE_BROWSER_CAMERA) {
        console.log('Using browser camera - no backend camera stop needed');
        setIsDetecting(false);
      } else {
        // Server camera mode - call backend to stop camera
        await axios.post(`${API_URL}/stop`);
        setIsDetecting(false);
      }
    } catch (error) {
      console.error('Error stopping detection:', error);
      alert('Failed to stop detection');
    } finally {
      setLoading(false);
    }
  };

  // Save frame
  const handleSaveFrame = async () => {
    try {
      const response = await axios.post(`${API_URL}/save-frame`);
      console.log('Frame saved successfully:', response.data);
      fetchSavedFrames();
      
      // Show success message
      if (response.data.filename) {
        alert(`✅ Frame saved: ${response.data.filename}`);
      }
    } catch (error) {
      console.error('Error saving frame:', error);
      
      // Show detailed error message
      let errorMsg = 'Failed to save frame';
      if (error.response?.data?.error) {
        errorMsg = error.response.data.error;
        if (error.response.data.details) {
          errorMsg += '\n\n' + error.response.data.details;
        }
      } else if (error.message) {
        errorMsg += '\n\n' + error.message;
      }
      
      alert(errorMsg);
    }
  };

  // Update confidence
  const handleConfidenceChange = async (newConfidence) => {
    try {
      await axios.post(`${API_URL}/confidence`, { confidence: newConfidence });
      setMetrics(prev => ({ ...prev, confidence: newConfidence }));
    } catch (error) {
      console.error('Error updating confidence:', error);
    }
  };

  // Delete frame
  const handleDeleteFrame = async (filename) => {
    try {
      await axios.delete(`${API_URL}/delete-frame/${filename}`);
      fetchSavedFrames();
    } catch (error) {
      console.error('Error deleting frame:', error);
      alert('Failed to delete frame');
    }
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <motion.header
        className="dashboard-header glass"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, type: "spring" }}
      >
        <div className="header-content">
          <motion.div 
            className="logo"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FaCamera className="logo-icon" />
            <h1 className="gradient-text">AI Object Detection</h1>
          </motion.div>

          <div className="header-actions">
            <motion.div
              className={`status-badge ${isDetecting ? 'active' : 'inactive'}`}
              animate={{
                scale: isDetecting ? [1, 1.1, 1] : 1,
              }}
              transition={{
                duration: 2,
                repeat: isDetecting ? Infinity : 0,
              }}
            >
              <span className="status-dot"></span>
              {isDetecting ? 'LIVE' : 'STOPPED'}
            </motion.div>

            <motion.button
              className="settings-btn glass-light"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowSettings(!showSettings)}
            >
              <FaCog />
            </motion.button>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className="dashboard-content">
        {/* Left Panel - Live Feed & Controls */}
        <div className="left-panel">
          <motion.div
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <LiveFeed isDetecting={isDetecting} />
          </motion.div>

          <motion.div
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <Controls
              isDetecting={isDetecting}
              onStart={handleStart}
              onStop={handleStop}
              onSaveFrame={handleSaveFrame}
              confidence={metrics.confidence}
              onConfidenceChange={handleConfidenceChange}
              loading={loading}
            />
          </motion.div>
        </div>

        {/* Middle Panel - Metrics */}
        <motion.div
          className="middle-panel"
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <MetricsPanel metrics={metrics} isDetecting={isDetecting} />
        </motion.div>

        {/* Right Panel - Saved Frames */}
        <motion.div
          className="right-panel"
          initial={{ x: 100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <SavedFrames 
            frames={savedFrames} 
            onDelete={handleDeleteFrame}
            onRefresh={fetchSavedFrames}
          />
        </motion.div>
      </div>

      {/* Settings Modal */}
      {showSettings && (
        <motion.div
          className="settings-modal"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setShowSettings(false)}
        >
          <motion.div
            className="settings-content glass"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2>Settings</h2>
            <div className="settings-info">
              <p><strong>Model:</strong> YOLOv8 Medium</p>
              <p><strong>Resolution:</strong> 640x480</p>
              <p><strong>Backend:</strong> Flask API</p>
              <p><strong>Version:</strong> 1.0.0</p>
            </div>
            <motion.button
              className="btn-primary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowSettings(false)}
            >
              Close
            </motion.button>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
}

export default Dashboard;

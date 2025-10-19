import React from 'react';
import { motion } from 'framer-motion';
import { FaPlay, FaPause, FaSave, FaPlus, FaMinus } from 'react-icons/fa';
import './Controls.css';

function Controls({ 
  isDetecting, 
  onStart, 
  onStop, 
  onSaveFrame, 
  confidence, 
  onConfidenceChange,
  loading 
}) {
  const handleConfidenceUp = () => {
    const newConf = Math.min(0.95, confidence + 0.05);
    onConfidenceChange(newConf);
  };

  const handleConfidenceDown = () => {
    const newConf = Math.max(0.05, confidence - 0.05);
    onConfidenceChange(newConf);
  };

  return (
    <div className="controls glass">
      <h2>Controls</h2>

      {/* Start/Stop Button */}
      <motion.button
        className={`control-btn ${isDetecting ? 'btn-stop' : 'btn-start'}`}
        onClick={isDetecting ? onStop : onStart}
        disabled={loading}
        whileHover={{ scale: loading ? 1 : 1.05 }}
        whileTap={{ scale: loading ? 1 : 0.95 }}
      >
        {loading ? (
          <div className="btn-loader"></div>
        ) : isDetecting ? (
          <>
            <FaPause /> Stop Detection
          </>
        ) : (
          <>
            <FaPlay /> Start Detection
          </>
        )}
      </motion.button>

      {/* Save Frame Button */}
      <motion.button
        className="control-btn btn-save"
        onClick={onSaveFrame}
        disabled={!isDetecting}
        whileHover={{ scale: isDetecting ? 1.05 : 1 }}
        whileTap={{ scale: isDetecting ? 0.95 : 1 }}
      >
        <FaSave /> Save Current Frame
      </motion.button>

      {/* Confidence Control */}
      <div className="confidence-control">
        <div className="control-header">
          <span>Confidence Threshold</span>
          <span className="confidence-value">{confidence.toFixed(2)}</span>
        </div>

        <div className="confidence-bar-container">
          <motion.div
            className="confidence-bar"
            initial={{ width: 0 }}
            animate={{ width: `${confidence * 100}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>

        <div className="confidence-buttons">
          <motion.button
            className="conf-btn"
            onClick={handleConfidenceDown}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            title="Lower confidence (more detections)"
          >
            <FaMinus />
          </motion.button>

          <input
            type="range"
            min="0.05"
            max="0.95"
            step="0.05"
            value={confidence}
            onChange={(e) => onConfidenceChange(parseFloat(e.target.value))}
            className="confidence-slider"
          />

          <motion.button
            className="conf-btn"
            onClick={handleConfidenceUp}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            title="Higher confidence (fewer detections)"
          >
            <FaPlus />
          </motion.button>
        </div>

        <div className="confidence-labels">
          <span>More Detections</span>
          <span>More Accurate</span>
        </div>
      </div>

      {/* Info */}
      <div className="controls-info">
        <p className="info-text">
          <strong>Tip:</strong> Lower confidence shows more objects, higher confidence shows only certain detections.
        </p>
      </div>
    </div>
  );
}

export default Controls;

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaImages, FaTrash, FaDownload, FaTimes, FaSync } from 'react-icons/fa';
import './SavedFrames.css';

function SavedFrames({ frames, onDelete, onRefresh }) {
  const [selectedFrame, setSelectedFrame] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const formatSize = (bytes) => {
    return (bytes / 1024).toFixed(1) + ' KB';
  };

  const handleDownload = (frame) => {
    const link = document.createElement('a');
    link.href = `http://localhost:5000${frame.url}`;
    link.download = frame.filename;
    link.click();
  };

  return (
    <div className="saved-frames glass">
      <div className="frames-header">
        <h2>
          <FaImages />
          <span>Saved Frames</span>
          <span className="frame-count">{frames.length}</span>
        </h2>
        <motion.button
          className="refresh-btn"
          onClick={onRefresh}
          whileHover={{ scale: 1.1, rotate: 180 }}
          whileTap={{ scale: 0.9 }}
          title="Refresh"
        >
          <FaSync />
        </motion.button>
      </div>

      <div className="frames-container">
        {frames.length === 0 ? (
          <motion.div
            className="frames-empty"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <FaImages className="empty-icon" />
            <h3>No Saved Frames</h3>
            <p>Captured frames will appear here</p>
          </motion.div>
        ) : (
          <div className="frames-grid">
            {frames.map((frame, index) => (
              <motion.div
                key={frame.filename}
                className="frame-card glass-light"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                whileHover={{ y: -5 }}
                onClick={() => setSelectedFrame(frame)}
              >
                <div className="frame-image-container">
                  <img
                    src={`http://localhost:5000${frame.url}`}
                    alt={frame.filename}
                    className="frame-image"
                  />
                  <div className="frame-overlay">
                    <motion.button
                      className="frame-action-btn delete"
                      onClick={(e) => {
                        e.stopPropagation();
                        if (window.confirm('Delete this frame?')) {
                          onDelete(frame.filename);
                        }
                      }}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      title="Delete"
                    >
                      <FaTrash />
                    </motion.button>
                    <motion.button
                      className="frame-action-btn download"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDownload(frame);
                      }}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      title="Download"
                    >
                      <FaDownload />
                    </motion.button>
                  </div>
                </div>
                <div className="frame-info">
                  <span className="frame-name" title={frame.filename}>
                    {frame.filename.slice(0, 20)}...
                  </span>
                  <span className="frame-size">{formatSize(frame.size)}</span>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Lightbox Modal */}
      <AnimatePresence>
        {selectedFrame && (
          <motion.div
            className="lightbox"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedFrame(null)}
          >
            <motion.div
              className="lightbox-content"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <motion.button
                className="lightbox-close"
                onClick={() => setSelectedFrame(null)}
                whileHover={{ scale: 1.1, rotate: 90 }}
                whileTap={{ scale: 0.9 }}
              >
                <FaTimes />
              </motion.button>

              <img
                src={`http://localhost:5000${selectedFrame.url}`}
                alt={selectedFrame.filename}
                className="lightbox-image"
              />

              <div className="lightbox-info glass">
                <div className="info-row">
                  <strong>Filename:</strong>
                  <span>{selectedFrame.filename}</span>
                </div>
                <div className="info-row">
                  <strong>Size:</strong>
                  <span>{formatSize(selectedFrame.size)}</span>
                </div>
                <div className="info-row">
                  <strong>Date:</strong>
                  <span>{formatDate(selectedFrame.created)}</span>
                </div>

                <div className="lightbox-actions">
                  <motion.button
                    className="btn-download"
                    onClick={() => handleDownload(selectedFrame)}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <FaDownload /> Download
                  </motion.button>
                  <motion.button
                    className="btn-delete"
                    onClick={() => {
                      if (window.confirm('Delete this frame?')) {
                        onDelete(selectedFrame.filename);
                        setSelectedFrame(null);
                      }
                    }}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <FaTrash /> Delete
                  </motion.button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default SavedFrames;

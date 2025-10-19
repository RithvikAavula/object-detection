import React from 'react';
import { motion } from 'framer-motion';
import { FaTachometerAlt, FaEye, FaCube, FaImages, FaSave } from 'react-icons/fa';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './MetricsPanel.css';

function MetricsPanel({ metrics, isDetecting }) {
  const [fpsHistory, setFpsHistory] = React.useState([]);

  React.useEffect(() => {
    if (isDetecting && metrics.fps > 0) {
      setFpsHistory(prev => {
        const newHistory = [...prev, { time: Date.now(), fps: metrics.fps }];
        return newHistory.slice(-20); // Keep last 20 points
      });
    } else {
      setFpsHistory([]);
    }
  }, [metrics.fps, isDetecting]);

  const metricCards = [
    {
      icon: FaTachometerAlt,
      label: 'FPS',
      value: metrics.fps.toFixed(1),
      color: 'var(--success)',
      gradient: 'linear-gradient(135deg, #10b981, #059669)',
    },
    {
      icon: FaEye,
      label: 'Confidence',
      value: metrics.confidence.toFixed(2),
      color: 'var(--accent)',
      gradient: 'linear-gradient(135deg, #ec4899, #db2777)',
    },
    {
      icon: FaCube,
      label: 'Objects',
      value: metrics.object_count,
      color: 'var(--warning)',
      gradient: 'linear-gradient(135deg, #f59e0b, #d97706)',
    },
    {
      icon: FaImages,
      label: 'Frames',
      value: metrics.frames_processed,
      color: 'var(--primary)',
      gradient: 'linear-gradient(135deg, #6366f1, #4f46e5)',
    },
    {
      icon: FaSave,
      label: 'Saved',
      value: metrics.saved_count,
      color: 'var(--secondary)',
      gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
    },
  ];

  return (
    <div className="metrics-panel">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Live Metrics
      </motion.h2>

      {/* Metric Cards */}
      <div className="metrics-grid">
        {metricCards.map((metric, index) => (
          <motion.div
            key={metric.label}
            className="metric-card glass-light glow-hover"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -5 }}
          >
            <div className="metric-icon" style={{ color: metric.color }}>
              <metric.icon />
            </div>
            <div className="metric-content">
              <span className="metric-label">{metric.label}</span>
              <motion.span
                className="metric-value"
                key={metric.value}
                initial={{ scale: 1.2, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                {metric.value}
              </motion.span>
            </div>
            <div 
              className="metric-bg"
              style={{ background: metric.gradient }}
            />
          </motion.div>
        ))}
      </div>

      {/* FPS Chart */}
      {isDetecting && fpsHistory.length > 2 && (
        <motion.div
          className="chart-container glass-light"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          transition={{ duration: 0.5 }}
        >
          <h3>FPS Performance</h3>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={fpsHistory}>
              <defs>
                <linearGradient id="fpsGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
              <XAxis 
                dataKey="time" 
                tick={false}
                stroke="rgba(148, 163, 184, 0.3)"
              />
              <YAxis 
                stroke="rgba(148, 163, 184, 0.3)"
                tick={{ fill: 'var(--text-secondary)' }}
              />
              <Tooltip 
                contentStyle={{
                  background: 'var(--glass)',
                  border: '1px solid var(--border)',
                  borderRadius: '8px',
                  color: 'var(--text)',
                }}
                formatter={(value) => [value.toFixed(1) + ' FPS', 'FPS']}
                labelFormatter={() => 'Real-time'}
              />
              <Area 
                type="monotone" 
                dataKey="fps" 
                stroke="#10b981" 
                strokeWidth={2}
                fill="url(#fpsGradient)" 
                animationDuration={300}
              />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>
      )}

      {/* Detected Objects */}
      {metrics.detections && Object.keys(metrics.detections).length > 0 && (
        <motion.div
          className="detections-list glass-light"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h3>Detected Objects</h3>
          <div className="detections-grid">
            {Object.entries(metrics.detections)
              .sort((a, b) => b[1] - a[1])
              .slice(0, 8)
              .map(([name, count], index) => (
                <motion.div
                  key={name}
                  className="detection-item"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <span className="detection-name">{name}</span>
                  <motion.span
                    className="detection-count"
                    key={count}
                    initial={{ scale: 1.5 }}
                    animate={{ scale: 1 }}
                  >
                    {count}
                  </motion.span>
                </motion.div>
              ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}

export default MetricsPanel;

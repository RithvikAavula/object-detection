# 🚀 Quick Start Guide - AI Object Detection Full Stack

## 📋 Prerequisites

Before you begin, make sure you have:
- ✅ **Python 3.8+** installed
- ✅ **Node.js 16+** and npm installed
- ✅ **Webcam** connected to your computer

---

## 🎯 Step-by-Step Setup

### Step 1: Run Setup Script

**Option A: Automated Setup (Recommended)**
```bash
# Double-click this file:
setup.bat

# Or run in terminal:
.\setup.bat
```

This will:
- Check Python and Node.js
- Create Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies

**Option B: Manual Setup**

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

---

### Step 2: Start the Application

**Option A: Easy Start (Recommended)**
```bash
# Double-click this file:
start.bat

# Or run in terminal:
.\start.bat
```

This opens:
- **Backend** in one terminal window
- **Frontend** in another terminal window

**Option B: Manual Start**

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

---

## 🌐 Access the Application

Once both servers are running:

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health

The browser should automatically open to http://localhost:3000

---

## 🎮 Using the Application

### 1. Start Detection
1. Click the green **"Start Detection"** button
2. Allow browser to access webcam (if prompted)
3. Wait 2-3 seconds for camera to initialize
4. You'll see live video with bounding boxes!

### 2. View Real-Time Metrics
Look at the metrics panel in the middle:
- **FPS**: Current frames per second
- **Confidence**: Detection threshold
- **Objects**: Number of objects detected right now
- **Frames**: Total frames processed
- **Saved**: Number of saved screenshots

### 3. Adjust Confidence
- Use **+** and **-** buttons or slide the slider
- **Lower confidence** (0.05-0.30): More detections, less accurate
- **Higher confidence** (0.50-0.95): Fewer detections, more accurate
- **Sweet spot**: 0.15-0.25 for most use cases

### 4. Save Frames
- Click **"Save Current Frame"** button
- Frame is saved with timestamp
- Appears in the gallery on the right
- Saved to `saved_frames/` folder

### 5. View Saved Frames
- Gallery shows all saved frames
- Click any frame to view full size
- **Download** button: Save to your computer
- **Delete** button: Remove frame
- Hover over thumbnail for quick actions

### 6. Stop Detection
- Click the red **"Stop Detection"** button
- Camera will be released
- All metrics freeze at current values

---

## 🎨 UI Features Explained

### Header
- **AI Object Detection** logo
- **Status badge**: Shows LIVE (green) or STOPPED (gray)
- **Settings button** (gear icon): View system info

### Live Feed Panel
- Shows real-time video with detections
- Green bounding boxes around objects
- Object labels with confidence scores
- "REC" badge when recording

### Metrics Panel
- **5 metric cards** with live updates
- **FPS chart** showing performance over time
- **Detected objects list** with counts
- All updates animate smoothly

### Controls Panel
- **Start/Stop** button with loading state
- **Save Frame** button (only active when detecting)
- **Confidence slider** with visual bar
- **+/- buttons** for quick adjustments
- **Tip section** for help

### Saved Frames Gallery
- Grid layout of all saved frames
- Frame counter badge
- Refresh button
- Click for lightbox view
- Hover for quick actions

---

## 🎯 What Objects Can Be Detected?

The system can detect **80 different object classes** from the COCO dataset:

**Common Objects:**
- person, bicycle, car, motorcycle, airplane, bus, train, truck, boat
- traffic light, fire hydrant, stop sign, parking meter, bench
- bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe
- backpack, umbrella, handbag, tie, suitcase
- frisbee, skis, snowboard, sports ball, kite, baseball bat, skateboard
- bottle, wine glass, cup, fork, knife, spoon, bowl
- banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake
- chair, couch, potted plant, bed, dining table, toilet
- TV, laptop, mouse, remote, keyboard, cell phone
- microwave, oven, toaster, sink, refrigerator
- book, clock, vase, scissors, teddy bear, hair drier, toothbrush

**Pro Tip:** Hold objects steady for 1-2 seconds for best detection!

---

## ⚙️ Troubleshooting

### Backend Won't Start

**Error: "ModuleNotFoundError: No module named 'flask'"**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Error: "Address already in use" (Port 5000)**
```bash
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Frontend Won't Start

**Error: "npm not found"**
- Install Node.js from https://nodejs.org/

**Error: "Module not found"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Error: Port 3000 in use**
```bash
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
set PORT=3001 && npm start
```

### Camera Issues

**No video showing:**
1. Check if camera is connected
2. Close other apps using camera (Zoom, Skype, etc.)
3. Check browser camera permissions
4. Restart backend server

**Camera permission denied:**
1. Browser should prompt for permission - click "Allow"
2. Check browser settings -> Privacy -> Camera
3. Make sure localhost has camera access

**Black screen:**
1. Try refreshing the page
2. Stop and start detection again
3. Check if camera works in other apps
4. Restart computer if needed

### Performance Issues

**Low FPS (below 15):**
1. Close other applications
2. Increase confidence threshold (fewer detections)
3. Check CPU usage in Task Manager
4. Make sure laptop is plugged in (not on battery)

**Lag or stuttering:**
1. Check network connection (shouldn't matter for localhost)
2. Clear browser cache
3. Close unused browser tabs
4. Restart both servers

### Detection Issues

**Not detecting objects:**
1. Lower confidence threshold (try 0.10-0.15)
2. Ensure good lighting
3. Hold objects closer to camera
4. Wait 1-2 seconds for detection
5. Check if object is in COCO dataset (see list above)

**Too many false detections:**
1. Increase confidence threshold (try 0.30-0.40)
2. Improve lighting conditions
3. Reduce background clutter

---

## 🛑 Stopping the Application

### Easy Way
Just close both terminal windows:
- Backend terminal (black window running Flask)
- Frontend terminal (showing React development server)

### Clean Way
In each terminal:
```bash
# Press Ctrl+C
# Servers will shut down gracefully
```

---

## 📊 System Requirements

### Minimum
- **CPU**: Dual-core 2.0 GHz
- **RAM**: 4 GB
- **GPU**: Not required (runs on CPU)
- **Disk**: 2 GB free space
- **Camera**: Any USB/built-in webcam

### Recommended
- **CPU**: Quad-core 2.5 GHz+
- **RAM**: 8 GB+
- **GPU**: Optional (CUDA support for faster processing)
- **Disk**: 5 GB+ free space
- **Camera**: 720p or higher

---

## 💡 Tips & Tricks

### Best Detection Results
1. **Good lighting** - Natural light or bright room
2. **Stable camera** - Don't move too much
3. **Close distance** - Objects 1-3 feet from camera
4. **Hold steady** - Keep objects still for 1-2 seconds
5. **Clean background** - Less clutter = better detection

### Performance Optimization
1. **Start with confidence 0.15** - Good balance
2. **Adjust as needed** - Higher for accuracy, lower for coverage
3. **Close unused apps** - Free up CPU/RAM
4. **Use wired connection** - For laptop webcam
5. **Check Task Manager** - Monitor resource usage

### Saving Frames
1. **Save interesting detections** - Build a collection
2. **Organized storage** - Auto-timestamped filenames
3. **Easy export** - Download from gallery
4. **Clean up regularly** - Delete old frames to save space

---

## 🎓 Learning Resources

### Understanding Confidence
- **0.05-0.20**: Very sensitive, many detections, some false positives
- **0.20-0.40**: Balanced, good for general use
- **0.40-0.60**: Conservative, high accuracy, may miss some objects
- **0.60-0.95**: Very strict, only very confident detections

### Reading the Metrics
- **FPS**: Higher is better (20-30 is great!)
- **Object Count**: Number of distinct objects right now
- **Frames Processed**: Total since start
- **Saved Count**: Your screenshot collection

### Understanding Bounding Boxes
- **Green boxes**: Detected objects
- **Label**: Object class name
- **Number**: Confidence score (0.00-1.00)
- **Thickness**: Same for all detections

---

## 🚀 Next Steps

Once you're comfortable:

1. **Experiment with confidence** - Find your sweet spot
2. **Try different objects** - Test the 80 COCO classes
3. **Build a collection** - Save interesting frames
4. **Monitor performance** - Watch the FPS chart
5. **Share your results** - Show friends your AI detection system!

---

## 📝 Quick Command Reference

```bash
# Setup
.\setup.bat                    # First time setup

# Start (Easy)
.\start.bat                    # Start both servers

# Start (Manual)
cd backend
venv\Scripts\activate
python app.py                  # Backend on :5000

cd frontend
npm start                      # Frontend on :3000

# Stop
Ctrl+C                        # In each terminal

# Standalone mode (no frontend)
python detection2.py          # Original script
```

---

## ✅ Success Checklist

Before starting:
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Webcam connected
- [ ] Setup script run successfully
- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Camera permission granted
- [ ] Video feed appears
- [ ] Detections working

If all checked - **you're ready to go!** 🎉

---

## 🆘 Still Having Issues?

1. **Check all prerequisites** are installed
2. **Run setup script** again
3. **Restart computer** (fixes many issues!)
4. **Try standalone mode** first (`python detection2.py`)
5. **Check console logs** for specific errors
6. **Review troubleshooting** section above

---

**Ready to detect objects with AI? Let's go! 🚀**

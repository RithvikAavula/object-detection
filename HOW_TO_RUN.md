# 🚀 HOW TO RUN FRONTEND & BACKEND

## ⚡ **QUICK START (Easiest Way)**

### First Time Setup (One Time Only)
```bash
.\setup.bat
```
**This will:**
- ✅ Install Python dependencies (Flask, OpenCV, YOLO)
- ✅ Install Node.js dependencies (React, Framer Motion)
- ✅ Takes ~5 minutes

### Start the Application (Every Time)
```bash
.\start.bat
```
**This will:**
- ✅ Start Flask backend on port 5000
- ✅ Start React frontend on port 3000
- ✅ Open browser automatically
- ✅ Two terminal windows appear

**That's it! 🎉**

---

## 📋 **DETAILED STEPS**

### Option 1: Automatic (Recommended) ⭐

#### 1️⃣ **First Time Setup**
Open PowerShell in project root:
```powershell
cd "E:\object detection"
.\setup.bat
```

Wait for installation to complete (~5 minutes)

#### 2️⃣ **Start Both Servers**
```powershell
.\start.bat
```

You'll see:
- ✅ Terminal 1: Flask backend starts
- ✅ Terminal 2: React frontend starts
- ✅ Browser opens to http://localhost:3000

#### 3️⃣ **Use the App**
- Click "Start Detection"
- Watch real-time object detection
- Save frames, adjust confidence
- View gallery

---

### Option 2: Manual (Separate Terminals)

#### **Terminal 1 - Backend (Flask)**
```powershell
# Navigate to project
cd "E:\object detection"

# Go to backend folder
cd backend

# Activate Python virtual environment
..\.venv\Scripts\Activate.ps1

# Start Flask server
python app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

✅ **Backend is now running on port 5000**

---

#### **Terminal 2 - Frontend (React)**
```powershell
# Navigate to project
cd "E:\object detection"

# Go to frontend folder
cd frontend

# Start React dev server
npm start
```

**Output:**
```
Compiled successfully!

Local:            http://localhost:3000
On Your Network:  http://192.168.x.x:3000
```

✅ **Frontend is now running on port 3000**

Browser will open automatically!

---

## 🎯 **Step-by-Step Visual Guide**

### 📦 **STEP 1: First Time Setup**

```
Open PowerShell → Navigate to project → Run setup
     ↓                    ↓                  ↓
E:\object detection → .\setup.bat → Wait 5 minutes
```

**What happens:**
1. Creates Python virtual environment (`.venv/`)
2. Installs Python packages (Flask, OpenCV, YOLO)
3. Installs Node.js packages (`node_modules/`)
4. Shows progress bars
5. Completes with success message

---

### 🚀 **STEP 2: Start Application**

```
Open PowerShell → Navigate to project → Run start
     ↓                    ↓                  ↓
E:\object detection → .\start.bat → Two terminals open
                                          ↓
                            Backend (5000) + Frontend (3000)
                                          ↓
                                Browser opens automatically
```

**What happens:**
1. Terminal 1 appears → Backend starts on port 5000
2. Terminal 2 appears → Frontend starts on port 3000
3. Browser opens to http://localhost:3000
4. You see the beautiful dashboard!

---

### 🎮 **STEP 3: Use the App**

```
Dashboard loads → Click "Start Detection" → Camera activates
       ↓                    ↓                      ↓
   Live feed          YOLO detects           Metrics update
       ↓                    ↓                      ↓
  Save frames        View gallery          Adjust confidence
```

---

## 🔧 **Troubleshooting**

### Problem: "setup.bat not found"
**Solution:** Make sure you're in the project root
```powershell
cd "E:\object detection"
.\setup.bat
```

---

### Problem: "Python not found"
**Solution:** Install Python first
1. Download Python 3.8+ from python.org
2. Install with "Add to PATH" checked
3. Restart terminal
4. Run `.\setup.bat` again

---

### Problem: "Node not found"
**Solution:** Install Node.js first
1. Download Node.js from nodejs.org
2. Install with default settings
3. Restart terminal
4. Run `.\setup.bat` again

---

### Problem: "Port 5000 already in use"
**Solution:** Stop other Flask apps
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Try starting again
.\start.bat
```

---

### Problem: "Port 3000 already in use"
**Solution:** Stop other React apps
```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Try starting again
.\start.bat
```

---

### Problem: "Camera not accessible"
**Solution:** Check camera permissions
1. Close other apps using camera (Zoom, Teams, etc.)
2. Check Windows camera permissions
3. Restart the application

---

## 📝 **Command Reference**

### Quick Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `.\setup.bat` | Install dependencies | First time only |
| `.\start.bat` | Start both servers | Every time |
| `python detection2.py` | Standalone CLI mode | No frontend needed |

### Manual Commands

#### Backend Commands
```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Start backend
cd backend
python app.py

# Stop backend
Ctrl + C
```

#### Frontend Commands
```powershell
# Start frontend
cd frontend
npm start

# Stop frontend
Ctrl + C

# Build for production
npm run build
```

---

## 🌐 **URLs to Access**

### Frontend (React Dashboard)
```
http://localhost:3000          ← Main URL
http://127.0.0.1:3000          ← Alternative
http://192.168.x.x:3000        ← Network access
```

### Backend (Flask API)
```
http://localhost:5000          ← API URL
http://localhost:5000/api/health   ← Health check
http://localhost:5000/api/status   ← Detection status
```

---

## ✅ **Success Indicators**

### Backend Started Successfully
You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
```

### Frontend Started Successfully
You should see:
```
webpack compiled successfully
Compiled successfully!

Local:            http://localhost:3000
On Your Network:  http://192.168.x.x:3000
```

Browser opens automatically with the dashboard!

---

## 🎨 **What You'll See**

### When Backend Starts
```
Terminal 1:
┌─────────────────────────────────┐
│ Flask Backend Server            │
│                                 │
│ Loading YOLO model...           │
│ ✓ Model loaded successfully     │
│                                 │
│ * Running on port 5000          │
│ * Press CTRL+C to quit          │
└─────────────────────────────────┘
```

### When Frontend Starts
```
Terminal 2:
┌─────────────────────────────────┐
│ React Development Server        │
│                                 │
│ Starting development server...  │
│ Compiled successfully!          │
│                                 │
│ http://localhost:3000           │
│                                 │
│ Browser opening...              │
└─────────────────────────────────┘
```

### When Browser Opens
```
Browser:
┌─────────────────────────────────────────┐
│  🎯 AI Object Detection Dashboard      │
│                                         │
│  [Loading animation...]                 │
│                                         │
│  ✨ Particle effects background        │
│  📊 Beautiful glassmorphism UI         │
│  🎬 Ready to detect!                   │
└─────────────────────────────────────────┘
```

---

## 🔄 **Complete Workflow**

### Day 1 (First Time)
```bash
# 1. Setup (one time)
.\setup.bat              # 5 minutes

# 2. Start
.\start.bat              # 30 seconds

# 3. Use the app
# Click "Start Detection"
# Watch live detection
# Save frames
# View gallery

# 4. Stop when done
# Ctrl+C in both terminals
```

### Day 2+ (Every Time After)
```bash
# Just run start!
.\start.bat              # 30 seconds

# Use the app
# Stop when done with Ctrl+C
```

---

## ⚡ **Pro Tips**

### Tip 1: Keep Terminals Open
- Don't close the terminal windows
- They show live logs
- Useful for debugging

### Tip 2: Check Logs
- Backend terminal shows API requests
- Frontend terminal shows compilation errors
- Read them if something goes wrong

### Tip 3: Restart if Needed
```bash
# In each terminal:
Ctrl + C           # Stop
python app.py      # Restart backend
npm start          # Restart frontend
```

### Tip 4: Use Standalone Mode
If frontend has issues, use CLI:
```bash
python detection2.py
```

### Tip 5: Check Health
Test if backend is running:
```bash
# In browser or new terminal
curl http://localhost:5000/api/health
```

---

## 📊 **Process Overview**

```
┌─────────────────────────────────────────────┐
│                                             │
│  YOU → .\start.bat                         │
│                                             │
│         ↓                                   │
│                                             │
│  ┌─────────────┐        ┌──────────────┐  │
│  │  Terminal 1  │        │  Terminal 2   │  │
│  │             │        │              │  │
│  │  Backend    │←─────→│  Frontend    │  │
│  │  (Python)   │  API   │  (React)     │  │
│  │  Port 5000  │        │  Port 3000   │  │
│  └─────────────┘        └──────────────┘  │
│         ↓                      ↓            │
│    Flask Server           React Dev        │
│         ↓                      ↓            │
│  REST API + Video        Beautiful UI      │
│                                             │
│         ↓                                   │
│                                             │
│  Browser → http://localhost:3000           │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎯 **Summary**

### Simplest Way ⭐
```bash
# First time
.\setup.bat

# Every time
.\start.bat
```

### Manual Way
```bash
# Terminal 1
cd backend
..\.venv\Scripts\Activate.ps1
python app.py

# Terminal 2
cd frontend
npm start
```

### Access
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:5000

---

<div align="center">

## 🎊 YOU'RE READY!

### Quick Start Commands

```bash
.\setup.bat    # First time only (5 minutes)
.\start.bat    # Every time (30 seconds)
```

**Browser opens automatically at http://localhost:3000**

### Need Help?

Read: `docs/GETTING_STARTED.md` for detailed guide

---

**Happy Detecting! 🎯✨**

</div>

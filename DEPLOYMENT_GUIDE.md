# 🚀 Deployment Guide - Render & Vercel

Complete guide to deploy your Object Detection application on **Render.com** and **Vercel**.

---

## 📋 **Table of Contents**

1. [Render Deployment](#render-deployment)
2. [Vercel Deployment](#vercel-deployment)
3. [Environment Variables](#environment-variables)
4. [Post-Deployment Setup](#post-deployment-setup)
5. [Troubleshooting](#troubleshooting)

---

## 🎯 **Render Deployment**

### **Option 1: Deploy Both (Full Stack)**

#### **Step 1: Prepare Your Repository**
```bash
# Make sure all files are committed
git add .
git commit -m "Add deployment configs"
git push origin main
```

#### **Step 2: Deploy on Render**

1. Go to [Render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

#### **What Gets Deployed:**
- ✅ **Backend Service** (Flask API) at `https://your-app-backend.onrender.com`
- ✅ **Frontend Service** (React) at `https://your-app-frontend.onrender.com`

---

### **Option 2: Deploy Backend Only**

#### **Manual Deployment:**

1. **Go to Render Dashboard**
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Configure:
   ```
   Name: object-detection-backend
   Region: Oregon (US West)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Instance Type: Free
   ```

5. **Add Environment Variables:**
   ```
   PYTHON_VERSION=3.11.0
   PORT=5000
   FLASK_ENV=production
   ```

6. Click **"Create Web Service"**

#### **After Deployment:**
- Backend URL: `https://your-backend.onrender.com`
- Health Check: `https://your-backend.onrender.com/api/health`

---

### **Deploy Frontend Separately**

1. **Go to Render Dashboard**
2. Click **"New +"** → **"Static Site"**
3. Configure:
   ```
   Name: object-detection-frontend
   Branch: main
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: build
   ```

4. **Add Environment Variable:**
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com
   ```

5. Click **"Create Static Site"**

---

## ⚡ **Vercel Deployment**

### **Option 1: Deploy Full Stack (Monorepo)**

#### **Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

#### **Step 2: Deploy**
```bash
# In project root
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name? object-detection-app
# - Directory? ./
# - Override settings? No
```

#### **Step 3: Set Environment Variables**
```bash
# In Vercel Dashboard
# Project Settings → Environment Variables

# Add:
REACT_APP_API_URL=https://your-backend-url.vercel.app
```

---

### **Option 2: Deploy Backend Only**

#### **Deploy Backend to Vercel:**

```bash
cd backend
vercel

# Configuration:
# - Project name: object-detection-backend
# - Directory: ./
```

**Important Notes:**
- ⚠️ **Vercel has limitations for Python/Flask apps**
- ⚠️ **Serverless functions timeout after 10 seconds (free plan)**
- ⚠️ **Not ideal for real-time video streaming**
- ✅ **Better to use Render for backend**

---

### **Deploy Frontend to Vercel (Recommended)**

```bash
cd frontend
vercel

# Configuration:
# - Framework: Create React App
# - Build Command: npm run build
# - Output Directory: build
```

#### **Set Environment Variable:**
```bash
# In Vercel Dashboard
REACT_APP_API_URL=https://your-render-backend.onrender.com
```

---

## 🔧 **Environment Variables**

### **Backend Environment Variables**

| Variable | Value | Platform |
|----------|-------|----------|
| `PYTHON_VERSION` | `3.11.0` | Render |
| `PORT` | `5000` | Render |
| `FLASK_ENV` | `production` | Both |
| `ALLOWED_ORIGINS` | `https://your-frontend-url.com` | Both |

### **Frontend Environment Variables**

| Variable | Value | Platform |
|----------|-------|----------|
| `REACT_APP_API_URL` | `https://your-backend-url.com` | Both |
| `NODE_VERSION` | `18.x` | Both |

---

## 🎨 **Recommended Deployment Strategy**

### **Best Approach:**

```
Backend  → Render.com (Better for real-time streaming)
Frontend → Vercel (Optimized for React/Static sites)
```

#### **Why?**
- ✅ **Render** handles long-running processes (video streaming)
- ✅ **Vercel** provides lightning-fast CDN for frontend
- ✅ Free tier on both platforms
- ✅ Easy to manage separately

---

## 📝 **Step-by-Step: Best Practice Deployment**

### **1. Deploy Backend on Render**

```bash
1. Go to render.com
2. New → Web Service
3. Connect GitHub repo
4. Root Directory: backend
5. Build: pip install -r requirements.txt
6. Start: gunicorn app:app
7. Add environment variables
8. Deploy!
```

**Result:** `https://object-detection-backend.onrender.com`

---

### **2. Deploy Frontend on Vercel**

```bash
cd frontend
vercel

# In Vercel Dashboard:
# Add environment variable:
REACT_APP_API_URL=https://object-detection-backend.onrender.com
```

**Result:** `https://object-detection-frontend.vercel.app`

---

### **3. Update Backend CORS**

Update `backend/app.py`:

```python
from flask_cors import CORS

app = Flask(__name__)

# Update CORS to allow your Vercel frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  # Local development
            "https://your-frontend.vercel.app",  # Production
            "https://*.vercel.app"  # All Vercel preview deployments
        ]
    }
})
```

---

### **4. Update Frontend API URL**

Create `frontend/.env.production`:

```env
REACT_APP_API_URL=https://object-detection-backend.onrender.com
```

---

## 🔍 **Post-Deployment Checklist**

### **Backend Health Check**
```bash
curl https://your-backend.onrender.com/api/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-10-19T...",
  "version": "1.0.0"
}
```

### **Frontend Check**
```bash
# Open in browser:
https://your-frontend.vercel.app

# Check console for API connection
# Should see successful API calls to backend
```

### **CORS Check**
```bash
# In browser console:
fetch('https://your-backend.onrender.com/api/status')
  .then(r => r.json())
  .then(console.log)

# Should return status without CORS error
```

---

## 🐛 **Troubleshooting**

### **Issue 1: CORS Error**

**Error:** `Access to fetch blocked by CORS policy`

**Solution:**
```python
# In backend/app.py
CORS(app, resources={
    r"/api/*": {
        "origins": "*"  # Allow all (for testing)
    }
})
```

---

### **Issue 2: Video Streaming Not Working**

**Problem:** Vercel serverless functions timeout

**Solution:** Use Render for backend (not Vercel)

---

### **Issue 3: Build Failing on Render**

**Error:** `Could not find opencv-python`

**Solution:** Use `opencv-python-headless` in requirements.txt (already done)

---

### **Issue 4: Frontend Can't Connect to Backend**

**Check:**
1. Is `REACT_APP_API_URL` set correctly?
2. Did you rebuild frontend after setting env var?
3. Is backend CORS allowing frontend domain?

**Fix:**
```bash
# Redeploy frontend with correct API URL
cd frontend
vercel --prod
```

---

## 📊 **Free Tier Limits**

### **Render Free Tier**
- ✅ 750 hours/month
- ✅ Spin down after 15 mins of inactivity
- ✅ Spin up time: ~30 seconds
- ⚠️ SSL included
- ⚠️ Custom domains supported

### **Vercel Free Tier**
- ✅ 100 GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Instant deployment
- ✅ Edge network (CDN)
- ✅ Custom domains supported

---

## 🎯 **Quick Commands**

### **Render Commands**
```bash
# View logs
render logs -t web -s your-service-name

# Restart service
render restart -s your-service-name
```

### **Vercel Commands**
```bash
# Deploy production
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls

# Remove deployment
vercel remove [deployment-url]
```

---

## 📱 **Testing Deployment**

### **1. Test Backend**
```bash
# Health check
curl https://your-backend.onrender.com/api/health

# Status check
curl https://your-backend.onrender.com/api/status
```

### **2. Test Frontend**
```bash
# Open in browser
https://your-frontend.vercel.app

# Test features:
✓ UI loads correctly
✓ Click "Start Detection"
✓ Check browser console for errors
✓ Verify API calls work
```

---

## 🔐 **Security Considerations**

### **Production Checklist**

1. **Update CORS Origins**
   ```python
   # Don't use origins="*" in production
   CORS(app, resources={
       r"/api/*": {
           "origins": ["https://your-actual-frontend.vercel.app"]
       }
   })
   ```

2. **Add Rate Limiting**
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(
       app,
       key_func=lambda: request.remote_addr,
       default_limits=["100 per hour"]
   )
   ```

3. **Environment Variables**
   - Never commit `.env` files
   - Use platform secrets management
   - Rotate keys regularly

---

## 📚 **Additional Resources**

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [React Production Build](https://create-react-app.dev/docs/production-build/)

---

## ✅ **Summary**

### **Recommended Setup:**
```
┌─────────────────────────────────┐
│  Frontend (Vercel)              │
│  https://app.vercel.app         │
│  - Lightning fast CDN           │
│  - Auto-scaling                 │
│  - Zero config                  │
└────────────┬────────────────────┘
             │ API Calls
             ▼
┌─────────────────────────────────┐
│  Backend (Render)               │
│  https://api.onrender.com       │
│  - Video streaming support      │
│  - Long-running processes       │
│  - Better for ML/CV apps        │
└─────────────────────────────────┘
```

---

<div align="center">

## 🎉 **Ready to Deploy!**

**All configuration files created:**
- ✅ `render.yaml` (Render Blueprint)
- ✅ `vercel.json` (Root config)
- ✅ `backend/vercel.json` (Backend config)
- ✅ `frontend/vercel.json` (Frontend config)
- ✅ `backend/wsgi.py` (Production entry point)
- ✅ Updated `requirements.txt` (Added gunicorn)

**Follow the guide above to deploy! 🚀**

</div>

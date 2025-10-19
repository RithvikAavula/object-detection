# 🏗️ Deployment Architecture

## 📊 **System Overview**

```
                    ┌─────────────────────────────┐
                    │      User's Browser          │
                    │  https://app.vercel.app      │
                    └──────────┬──────────────────┘
                               │
                               │ HTTPS Requests
                               │
              ┌────────────────┴───────────────────┐
              │                                    │
              ▼                                    ▼
    ┌─────────────────┐                 ┌──────────────────┐
    │   Vercel CDN    │                 │  Render Server   │
    │   (Frontend)    │────API Calls───▶│   (Backend)      │
    │                 │                 │                  │
    │  React App      │                 │  Flask + YOLO    │
    │  Static Files   │                 │  Video Stream    │
    │  Edge Network   │                 │  WebSocket       │
    └─────────────────┘                 └──────────────────┘
```

---

## 🌐 **Deployment Flow**

### **Frontend Deployment (Vercel)**

```
┌──────────────┐
│  Developer   │
│  Push Code   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  GitHub Repo     │
│  (main branch)   │
└──────┬───────────┘
       │
       │ Webhook Trigger
       ▼
┌──────────────────────────┐
│  Vercel Build Server     │
│  1. npm install          │
│  2. npm run build        │
│  3. Optimize assets      │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Vercel Edge Network     │
│  - Global CDN            │
│  - 99.99% uptime         │
│  - Instant deployment    │
│  URL: xxx.vercel.app     │
└──────────────────────────┘
```

### **Backend Deployment (Render)**

```
┌──────────────┐
│  Developer   │
│  Push Code   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  GitHub Repo     │
│  (main branch)   │
└──────┬───────────┘
       │
       │ Webhook Trigger
       ▼
┌──────────────────────────┐
│  Render Build Server     │
│  1. pip install          │
│  2. Download models      │
│  3. Setup environment    │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Render Web Service      │
│  - Gunicorn server       │
│  - Python 3.11           │
│  - Always-on or sleep    │
│  URL: xxx.onrender.com   │
└──────────────────────────┘
```

---

## 🔄 **Request Flow**

### **1. Initial Page Load**

```
User
  │
  ├──▶ DNS Lookup (vercel.app)
  │
  └──▶ Vercel Edge Server (Nearest CDN)
        │
        ├──▶ Serve index.html
        ├──▶ Serve JS bundles
        ├──▶ Serve CSS files
        └──▶ Serve images/assets
              │
              └──▶ Browser renders React app
```

### **2. API Request Flow**

```
React App (Vercel)
  │
  ├──▶ fetch('/api/status')
  │
  └──▶ HTTPS Request
        │
        └──▶ Render Backend
              │
              ├──▶ Flask receives request
              ├──▶ Process with YOLO
              ├──▶ Generate response
              └──▶ Send JSON back
                    │
                    └──▶ React updates UI
```

### **3. Video Streaming Flow**

```
User clicks "Start Detection"
  │
  └──▶ POST /api/start
        │
        └──▶ Backend starts camera
              │
              ├──▶ Capture frame (30 FPS)
              ├──▶ YOLO detection (15 FPS)
              ├──▶ Draw boxes & labels
              └──▶ Stream MJPEG
                    │
                    └──▶ GET /api/video-feed
                          │
                          └──▶ <img> tag in React
                                │
                                └──▶ Continuous stream
```

---

## 🗂️ **File Structure on Each Platform**

### **Vercel (Frontend)**

```
vercel.app/
├── index.html
├── static/
│   ├── css/
│   │   └── main.[hash].css
│   ├── js/
│   │   ├── main.[hash].js
│   │   └── runtime.[hash].js
│   └── media/
│       └── logo.[hash].png
└── asset-manifest.json
```

### **Render (Backend)**

```
/opt/render/project/src/backend/
├── app.py
├── wsgi.py
├── requirements.txt
├── yolov8m.pt
└── __pycache__/
```

---

## 🔐 **Security Architecture**

```
┌──────────────────────────────────────┐
│  User's Browser                      │
│  - HTTPS only                        │
│  - No sensitive data stored          │
└──────────┬───────────────────────────┘
           │
           │ TLS 1.3 Encrypted
           │
┌──────────▼───────────────────────────┐
│  Vercel CDN                          │
│  - Auto SSL certificate              │
│  - DDoS protection                   │
│  - Rate limiting                     │
└──────────┬───────────────────────────┘
           │
           │ HTTPS Only
           │
┌──────────▼───────────────────────────┐
│  Render Backend                      │
│  - CORS validation                   │
│  - API rate limiting                 │
│  - Environment variables (secrets)   │
│  - No exposed ports except 5000      │
└──────────────────────────────────────┘
```

---

## 📈 **Scaling Architecture**

### **Current Setup (Free Tier)**

```
Load: 1-100 concurrent users
│
├──▶ Frontend (Vercel)
│     └──▶ Auto-scaling (unlimited)
│
└──▶ Backend (Render)
      └──▶ Single instance
            └──▶ Max: ~10 simultaneous streams
```

### **Scaled Setup (Paid Tier)**

```
Load: 100-1000 concurrent users
│
├──▶ Frontend (Vercel Pro)
│     └──▶ Auto-scaling (unlimited)
│     └──▶ Edge caching
│
└──▶ Backend (Render Standard)
      ├──▶ Multiple instances
      ├──▶ Load balancer
      └──▶ Max: ~100 simultaneous streams
```

---

## 🌍 **Global Distribution**

### **Vercel CDN Locations**

```
User Location          Nearest CDN
─────────────────────────────────────
🇺🇸 USA               Washington, Dallas, SF
🇪🇺 Europe            London, Frankfurt
🇦🇺 Asia-Pacific     Singapore, Tokyo, Sydney
🇧🇷 South America    São Paulo
🇮🇳 India             Mumbai
```

### **Render Server Locations**

```
Region                 Location
──────────────────────────────────
oregon                 Portland, USA
frankfurt              Frankfurt, Germany
singapore              Singapore
```

---

## 💾 **Data Flow**

### **Frame Processing Pipeline**

```
┌────────────────┐
│  Camera        │
│  640x480 @ 30  │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  OpenCV Read   │
│  RGB → BGR     │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  YOLO v8       │
│  Detection     │
│  (every 2nd)   │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  Draw Boxes    │
│  Colorful      │
│  Labels        │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  JPEG Encode   │
│  85% Quality   │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  MJPEG Stream  │
│  HTTP/1.1      │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  Browser       │
│  <img> tag     │
└────────────────┘
```

---

## 🔄 **CI/CD Pipeline**

```
Developer
   │
   └──▶ git push origin main
          │
          ├──────────────────┬──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
   ┌──────────┐      ┌──────────┐      ┌──────────┐
   │ GitHub   │      │ Vercel   │      │ Render   │
   │ Webhook  │───▶  │ Build    │      │ Build    │
   └──────────┘      └────┬─────┘      └────┬─────┘
                          │                  │
                          ▼                  ▼
                    ┌──────────┐      ┌──────────┐
                    │ Deploy   │      │ Deploy   │
                    │ Frontend │      │ Backend  │
                    └────┬─────┘      └────┬─────┘
                         │                  │
                         └────────┬─────────┘
                                  │
                                  ▼
                            ┌──────────┐
                            │ LIVE! 🎉 │
                            └──────────┘
```

---

## 📊 **Performance Metrics**

### **Target Performance**

| Metric | Target | Platform |
|--------|--------|----------|
| **Page Load** | < 2 seconds | Vercel |
| **API Response** | < 100ms | Render |
| **Video Latency** | < 50ms | Render |
| **FPS** | 30+ | Backend |
| **Detection FPS** | 15+ | Backend |
| **Uptime** | 99.9% | Both |

---

## 🎯 **Resource Usage**

### **Backend (Render)**

```
CPU: 0.5 cores (1 instance)
RAM: 512 MB
Storage: 1 GB
Bandwidth: 100 GB/month (free)
```

### **Frontend (Vercel)**

```
Build Time: ~2 minutes
Bundle Size: ~2 MB (gzipped)
Bandwidth: 100 GB/month (free)
CDN: Global (50+ locations)
```

---

## 🔧 **Environment Configuration**

```
┌─────────────────────────────────────┐
│  Vercel Dashboard                   │
│  ├── REACT_APP_API_URL              │
│  └── NODE_VERSION                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Render Dashboard                   │
│  ├── PYTHON_VERSION                 │
│  ├── FLASK_ENV                      │
│  ├── PORT                           │
│  └── ALLOWED_ORIGINS                │
└─────────────────────────────────────┘
```

---

## 🚀 **Deployment Comparison**

| Aspect | Render | Vercel |
|--------|--------|--------|
| **Deploy Time** | 3-5 min | 1-2 min |
| **Cold Start** | 30 sec | Instant |
| **Build Cache** | ✅ Yes | ✅ Yes |
| **Auto Deploy** | ✅ Yes | ✅ Yes |
| **Preview Deploy** | ❌ No | ✅ Yes |
| **Rollback** | ✅ Yes | ✅ Yes |
| **Logs** | ✅ Live | ✅ Live |
| **Monitoring** | ✅ Basic | ✅ Advanced |

---

<div align="center">

## 🏗️ **Architecture Summary**

**Frontend:** Vercel CDN (Global)  
**Backend:** Render Server (Oregon)  
**Database:** None (stateless)  
**Storage:** Local filesystem  
**SSL:** Auto-generated (both)  
**Domain:** Free subdomain (both)  

**Status:** ✅ Production Ready

</div>

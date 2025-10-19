# 🚀 Quick Deployment Checklist

## ✅ Pre-Deployment

- [ ] All code committed to GitHub
- [ ] `.gitignore` updated (don't commit `.env`, `node_modules`, `__pycache__`)
- [ ] `requirements.txt` includes all dependencies
- [ ] `package.json` has correct scripts

---

## 📦 **Files Created**

✅ **Root Directory:**
- `render.yaml` - Render Blueprint configuration
- `vercel.json` - Vercel monorepo configuration
- `DEPLOYMENT_GUIDE.md` - Complete deployment guide
- `DEPLOYMENT_CHECKLIST.md` - This file

✅ **Backend Directory:**
- `backend/vercel.json` - Backend-specific Vercel config
- `backend/wsgi.py` - Production WSGI entry point
- `backend/requirements.txt` - Updated with gunicorn

✅ **Frontend Directory:**
- `frontend/vercel.json` - Frontend-specific Vercel config

---

## 🎯 **Recommended: Backend on Render, Frontend on Vercel**

### **Backend (Render.com)**

1. **Go to Render Dashboard**
   - https://dashboard.render.com

2. **New Web Service**
   - Connect GitHub repo
   - Name: `object-detection-backend`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Environment Variables**
   ```
   PYTHON_VERSION=3.11.0
   PORT=5000
   FLASK_ENV=production
   ```

4. **Deploy!**
   - Wait ~5 minutes
   - Note your backend URL: `https://xxx.onrender.com`

---

### **Frontend (Vercel)**

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy Frontend**
   ```bash
   cd frontend
   vercel
   ```

3. **Add Environment Variable in Vercel Dashboard**
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com
   ```

4. **Redeploy**
   ```bash
   vercel --prod
   ```

---

## 🔧 **Update CORS in Backend**

Edit `backend/app.py`:

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://your-frontend.vercel.app",
            "https://*.vercel.app"
        ]
    }
})
```

Commit and push to trigger auto-deployment on Render.

---

## ✅ **Testing Deployment**

### **Backend Test**
```bash
curl https://your-backend.onrender.com/api/health
```

Expected:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-19...",
  "version": "1.0.0"
}
```

### **Frontend Test**
1. Open `https://your-frontend.vercel.app`
2. Click "Start Detection"
3. Check browser console for errors
4. Verify video stream works

---

## 🐛 **Common Issues**

### **CORS Error**
- Update `backend/app.py` CORS origins
- Redeploy backend

### **API Not Found**
- Check `REACT_APP_API_URL` in Vercel dashboard
- Must include `https://` protocol
- Rebuild frontend after env var change

### **Video Not Working**
- Backend must be on Render (not Vercel)
- Vercel serverless has timeout limits

### **Render Service Sleeping**
- Free tier spins down after 15 mins
- First request takes ~30 seconds to wake up
- Upgrade to paid plan for always-on

---

## 📝 **Environment Variables**

### **Backend (Render)**
```env
PYTHON_VERSION=3.11.0
PORT=5000
FLASK_ENV=production
```

### **Frontend (Vercel)**
```env
REACT_APP_API_URL=https://your-backend.onrender.com
```

---

## 🎉 **Deployment Complete!**

Once deployed:
- ✅ Backend: `https://your-backend.onrender.com`
- ✅ Frontend: `https://your-frontend.vercel.app`
- ✅ Health: `https://your-backend.onrender.com/api/health`

---

## 📚 **Next Steps**

1. **Custom Domain** (Optional)
   - Add custom domain in Render/Vercel dashboard
   - Update DNS records

2. **Monitoring**
   - Check Render logs for backend issues
   - Check Vercel logs for frontend issues

3. **Updates**
   - Push to GitHub → Auto-deploys on both platforms
   - Monitor build logs

---

<div align="center">

## 🚀 **All Set for Deployment!**

**Read full guide:** `DEPLOYMENT_GUIDE.md`

**Start deploying now! 🎯**

</div>

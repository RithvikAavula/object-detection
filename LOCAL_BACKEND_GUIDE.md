# Run Backend Locally with Camera Support

Since Render servers don't have camera access, you can run the backend locally while keeping the frontend deployed.

## Quick Start

### 1. Run Backend Locally
```bash
cd backend
python app.py
```
Backend will start at: `http://localhost:5000`

### 2. Update Frontend to Use Local Backend

Create `frontend/.env.local`:
```env
REACT_APP_API_URL=http://localhost:5000
```

### 3. Run Frontend Locally (or use deployed version)
```bash
cd frontend
npm start
```

## Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  Your Computer  │         │   Render Cloud   │
│                 │         │                  │
│  📹 Camera      │         │  🌐 Frontend     │
│  ↓              │         │  (Static Site)   │
│  🖥️  Backend    │←────────┤                  │
│  (localhost)    │  API    │                  │
└─────────────────┘         └──────────────────┘
```

## Benefits

✅ **Camera access** - Full webcam support
✅ **Faster processing** - Local GPU/CPU
✅ **No deployment delays** - Instant updates
✅ **Free** - No Render resource limits

## Security Note

If you want others to access your local backend:
1. Use ngrok: `ngrok http 5000`
2. Update frontend .env with ngrok URL
3. Update CORS in backend/app.py with ngrok URL

## Alternative: Deploy Frontend Locally Too

If you want everything local with camera support:

```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend  
cd frontend
npm start
```

Access at: `http://localhost:3000`

# 📹 WebRTC Browser Camera Detection

## Overview

Your object detection system now supports **TWO camera modes**:

### Mode 1: Server Camera (Original)
- Backend accesses `/dev/video0` on the server
- ❌ **Doesn't work on cloud** (Render, Heroku, etc.)
- ✅ Works locally with webcam

### Mode 2: Browser Camera (NEW - WebRTC) ⭐
- Frontend captures camera via browser's `getUserMedia()`
- Sends frames to backend for processing
- ✅ **Works on cloud deployment!**
- ✅ Uses the **user's camera**, not server's

---

## How It Works

```
┌─────────────────────────────────────────────────────┐
│                   User's Browser                     │
│                                                      │
│  1. getUserMedia() → Request camera access          │
│  2. <video> element → Capture live feed             │
│  3. <canvas> → Draw frame                           │
│  4. toBlob() → Convert to JPEG                      │
│  5. fetch() → Send to backend                       │
│                                                      │
│                       ↓ (10 FPS)                     │
├──────────────────────────────────────────────────────┤
│                   Backend Server                     │
│                  (Render / Local)                    │
│                                                      │
│  6. Receive frame via /api/process-frame            │
│  7. YOLO model → Detect objects                     │
│  8. Draw bounding boxes                              │
│  9. Return processed frame                           │
│                                                      │
│                       ↓                              │
├──────────────────────────────────────────────────────┤
│                   User's Browser                     │
│                                                      │
│  10. Display processed frame with detections         │
│  11. Update metrics (FPS, object count, etc.)       │
└──────────────────────────────────────────────────────┘
```

---

## Switching Between Modes

In `frontend/src/components/LiveFeed.js`, line 7:

```javascript
const USE_BROWSER_CAMERA = true; // Toggle mode
```

**Settings:**
- `true` → Browser camera (WebRTC) - **Works on cloud!** ✅
- `false` → Server camera (MJPEG) - Only works locally ❌

---

## Benefits of Browser Camera Mode

| Feature | Server Camera | Browser Camera |
|---------|--------------|----------------|
| **Works on Render** | ❌ No | ✅ **Yes!** |
| **Works on Heroku** | ❌ No | ✅ **Yes!** |
| **Works Locally** | ✅ Yes | ✅ Yes |
| **Uses User's Camera** | ❌ No | ✅ **Yes!** |
| **No Server Hardware Needed** | ❌ Needs webcam | ✅ **Any camera!** |
| **Mobile Support** | ❌ No | ✅ **Yes!** |
| **Tablet Support** | ❌ No | ✅ **Yes!** |

---

## Browser Compatibility

### ✅ Supported Browsers:
- Chrome/Edge (Desktop & Mobile)
- Firefox (Desktop & Mobile)
- Safari (Desktop & iOS)
- Opera
- Samsung Internet

### Camera Access Requirements:
1. **HTTPS required** (or localhost)
2. User must **grant permission**
3. Browser must support `getUserMedia()`

---

## Deployment Configurations

### Configuration 1: Fully Cloud (WebRTC) ⭐ RECOMMENDED
```
Frontend: Render → https://object-detection-2-9oo8.onrender.com/
Backend: Render → https://object-detection-rirh.onrender.com
Camera: User's browser
```

**Setup:**
1. Set `USE_BROWSER_CAMERA = true` in LiveFeed.js
2. Deploy to Render
3. ✅ **Camera works!**

---

### Configuration 2: Local Development
```
Frontend: localhost:3000
Backend: localhost:5000
Camera: User's browser OR Server camera
```

**Setup:**
```bash
.\start_with_camera.bat
```

Choose camera mode by setting `USE_BROWSER_CAMERA`.

---

### Configuration 3: Hybrid (Local Backend + Cloud Frontend)
```
Frontend: Render → https://object-detection-2-9oo8.onrender.com/
Backend: Local → http://localhost:5000
Camera: User's browser OR Server camera
```

**Setup:**
1. Run backend: `cd backend && python app.py`
2. Frontend points to `http://localhost:5000`
3. Both camera modes work!

---

## API Endpoint

### POST `/api/process-frame`

**Purpose:** Process a single frame from browser camera

**Request:**
```http
POST /api/process-frame
Content-Type: multipart/form-data

frame: [JPEG image blob]
```

**Response:**
```http
200 OK
Content-Type: image/jpeg

[Processed JPEG with bounding boxes]
```

**Features:**
- Uses current confidence threshold
- Updates metrics (object count, detections)
- Returns frame with drawn bounding boxes
- Same YOLO model as server camera

---

## Performance

### Server Camera Mode (MJPEG):
- **FPS:** 20-30 (limited by camera)
- **Latency:** ~50ms
- **Bandwidth:** High (continuous stream)

### Browser Camera Mode (WebRTC):
- **FPS:** 10 (configurable, line 33 in LiveFeed.js)
- **Latency:** ~100-200ms (includes network)
- **Bandwidth:** Medium (10 frames/sec)

**To adjust FPS:**
```javascript
// In LiveFeed.js, line 33
const interval = setInterval(() => {
  captureAndSendFrame();
}, 100); // 100ms = 10 FPS, 50ms = 20 FPS, etc.
```

---

## Camera Permission

When user clicks "Start Detection" with browser camera mode:

1. **Browser shows permission dialog:**
   ```
   https://object-detection-2-9oo8.onrender.com wants to:
   
   [📹] Use your camera
   
   [Block] [Allow]
   ```

2. **User clicks "Allow"**

3. **Camera starts** → Frontend captures frames → Backend processes → Display results

### Handling Permission Denied:

If user clicks "Block", the error message shows:
```
Camera Error: Permission denied
Please allow camera access in your browser
```

**To fix:**
1. Click the 🔒 lock icon in address bar
2. Set Camera to "Allow"
3. Refresh page

---

## Mobile Support

### ✅ Browser Camera Mode works on mobile!

**Features:**
- Front camera (selfie)
- Back camera (rear)
- Automatic camera selection
- Touch-friendly UI

**To switch cameras:**

Modify `LiveFeed.js`, line 19:
```javascript
video: {
  width: { ideal: 640 },
  height: { ideal: 480 },
  facingMode: 'user'  // 'user' = front, 'environment' = back
}
```

---

## Troubleshooting

### Issue: "Camera Error: Permission denied"
**Solution:** Allow camera access in browser settings

### Issue: "Camera Error: Not found"
**Solution:** Check if device has a camera, try another browser

### Issue: "Model not loaded"
**Solution:** Wait for backend to finish loading YOLO model

### Issue: Black screen
**Solution:** 
1. Check browser console for errors
2. Verify HTTPS (required for camera access)
3. Try refreshing page

### Issue: Low FPS
**Solution:** Reduce frame send rate in LiveFeed.js (increase interval)

---

## Testing

### Test Browser Camera Locally:
```bash
cd frontend
npm start
```
Open `http://localhost:3000` and click "Start Detection"

### Test on Deployed Site:
1. Visit https://object-detection-2-9oo8.onrender.com/
2. Click "Start Detection"
3. Allow camera access
4. ✅ See detection working with your camera!

---

## Security & Privacy

### Camera Access:
- ✅ User must explicitly grant permission
- ✅ Only works on HTTPS or localhost
- ✅ Frames are processed and discarded immediately
- ✅ No frames are stored on server (unless user clicks "Save")
- ✅ Camera indicator shows when active

### Data Flow:
1. Camera → Browser (local)
2. Browser → Backend (HTTPS encrypted)
3. Backend processes → Returns result
4. Backend discards frame (no storage)

---

## Comparison: Server vs Browser Camera

| Aspect | Server Camera | Browser Camera |
|--------|--------------|----------------|
| **Deployment** | Local only | ✅ **Cloud works!** |
| **Setup Complexity** | Medium | Easy |
| **Camera Required On** | Server | User's device |
| **Mobile Support** | ❌ No | ✅ Yes |
| **Privacy** | Server sees camera | User controls camera |
| **FPS** | Higher (20-30) | Lower (10-15) |
| **Latency** | Lower (~50ms) | Higher (~150ms) |
| **Bandwidth** | High | Medium |
| **Use Case** | Fixed camera setup | User-facing app |

---

## Summary

### ✅ With Browser Camera (WebRTC):
- Works on **Render, Heroku, any cloud platform**
- Uses **user's camera** (laptop, phone, tablet)
- **No server camera needed**
- Perfect for **public-facing applications**
- **Mobile-friendly**

### This Solves the Original Problem!

**Before:** ❌ "Render doesn't have a camera"

**After:** ✅ "Render doesn't need a camera - we use the user's camera instead!"

---

## Next Steps

1. **Deploy to Render** with `USE_BROWSER_CAMERA = true`
2. **Test on your deployed site**
3. **Share the link** - anyone can use their camera!
4. **Try on mobile** - works great!

Your object detection is now **fully cloud-compatible** with camera support! 🎉📹

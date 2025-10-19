# Object Detection - Screen Layout

## 📺 What You'll See On Screen

```
╔═══════════════════════════════════════════════════════════════╗
║                    DETECTION WINDOW                            ║
║  ┌──────────────────────┐                                     ║
║  │ [Semi-transparent]   │                                     ║
║  │ FPS: 25         ●    │  👤 person                          ║
║  │ Objects: 3      ●    │  ┌─────────────────┐               ║
║  │ Frames: 1523    ●    │  │                 │               ║
║  │ Saved: 5        ●    │  │   [person 98%]  │               ║
║  │                      │  └─────────────────┘               ║
║  │ Current:             │                                     ║
║  │   person: 2          │         📱 phone                    ║
║  │   phone: 1           │         ┌──────┐                   ║
║  │   laptop: 1          │         │phone │                   ║
║  └──────────────────────┘         │ 92%  │                   ║
║                                    └──────┘                   ║
║                                                                ║
║                          💻 laptop                             ║
║                     ┌─────────────────────┐                   ║
║                     │                     │                   ║
║                     │  [laptop 95%]       │                   ║
║                     │                     │                   ║
║                     └─────────────────────┘                   ║
║                                                                ║
╚═══════════════════════════════════════════════════════════════╝
      Window Title: "Object Detection - Press 'q' to quit, 's' to save"
```

---

## 🎨 Color Guide

### Info Panel Colors:
- **FPS: 25** → Bright Green (0, 255, 0)
- **Objects: 3** → Yellow (255, 255, 0)
- **Frames: 1523** → Orange (255, 200, 100)
- **Saved: 5** → Light Blue (100, 200, 255)
- **Current:** → Light Gray (200, 200, 200)
- **Object names** → Light Green (150, 255, 150)

### Bounding Boxes:
- Different colors for different object types
- Auto-assigned by YOLO
- Labels show confidence percentage

---

## 📏 Panel Dimensions

```
Info Panel:
┌─────────────────────────┐
│ Width: 280 pixels       │
│ Height: ~200 pixels     │
│ Position: (5, 5)        │
│ Background: Black       │
│ Transparency: 60%       │
└─────────────────────────┘
```

---

## 📁 File Structure After Running

```
E:\object detection\
│
├── detection2.py          ← Your main script
├── yolov5su.pt           ← YOLO model
│
└── saved_frames\          ← AUTO-CREATED
    ├── detection_20251019_143052_frame123.jpg
    ├── detection_20251019_143055_frame145.jpg
    └── detection_20251019_143058_frame167.jpg
```

---

## 🎮 Interactive Elements

### Keyboard Controls:
```
┌────────┬──────────────────────────────────┐
│  Key   │           Action                 │
├────────┼──────────────────────────────────┤
│   s    │ Save current frame               │
│        │ → Creates timestamped file       │
│        │ → Increments "Saved" counter     │
│        │ → Shows confirmation message     │
├────────┼──────────────────────────────────┤
│   q    │ Quit application                 │
│        │ → Shows session summary          │
│        │ → Lists all statistics           │
│        │ → Closes cleanly                 │
└────────┴──────────────────────────────────┘
```

---

## 📊 Metrics Explanation

### Real-Time Counters:

1. **FPS (Frames Per Second)**
   ```
   FPS: 25
   ↓
   Higher = Smoother (20-30 is good)
   ```

2. **Objects (Current Frame)**
   ```
   Objects: 3
   ↓
   How many objects detected RIGHT NOW
   ```

3. **Frames (Total Processed)**
   ```
   Frames: 1523
   ↓
   Total frames since starting
   ```

4. **Saved (Screenshot Count)**
   ```
   Saved: 5
   ↓
   Number of times you pressed 's'
   ```

5. **Current (Object Breakdown)**
   ```
   Current:
     person: 2    ← 2 people visible
     phone: 1     ← 1 phone visible
     laptop: 1    ← 1 laptop visible
   ```

---

## 💾 Save Action Visualization

### When you press 's':

```
BEFORE:                    AFTER:
Saved: 4                   Saved: 5  ← Increments
                           
Console:
✓ Frame saved: saved_frames/detection_20251019_143052_frame123.jpg

File System:
saved_frames\
  └── detection_20251019_143052_frame123.jpg  ← NEW!
```

---

## 🔄 Real-Time Updates

### What Updates Every Frame:

```
[CONSTANT UPDATE]          [ACCUMULATIVE]
- FPS counter             - Total frames
- Objects count           - Saved count  
- Current object list     - Object statistics
- Bounding boxes          
```

---

## 📈 Example Session Flow

### Startup:
```
1. Script starts
2. Creates "saved_frames" folder (if needed)
3. Loads YOLO model
4. Opens webcam
5. Shows controls info
6. Detection window appears
```

### During Use:
```
Frame 1:  FPS: 0   Objects: 0   Saved: 0
Frame 50: FPS: 25  Objects: 2   Saved: 0
[Press 's']
Frame 51: FPS: 25  Objects: 2   Saved: 1  ✓
Frame 100: FPS: 24 Objects: 3   Saved: 1
[Press 's']
Frame 101: FPS: 24 Objects: 3   Saved: 2  ✓
```

### Exit:
```
[Press 'q']
→ Detection window closes
→ Console shows full summary
→ All resources released
```

---

## 🎯 Practical Examples

### Example 1: Office Desk Detection
```
┌─────────────────┐
│ FPS: 28         │
│ Objects: 5      │
│ Frames: 234     │
│ Saved: 2        │
│                 │
│ Current:        │
│   laptop: 2     │  ← 2 laptops on desk
│   keyboard: 2   │  ← 2 keyboards
│   mouse: 1      │  ← 1 mouse
└─────────────────┘
```

### Example 2: Meeting Room
```
┌─────────────────┐
│ FPS: 26         │
│ Objects: 8      │
│ Frames: 567     │
│ Saved: 4        │
│                 │
│ Current:        │
│   person: 5     │  ← 5 people in meeting
│   chair: 2      │  ← 2 visible chairs
│   laptop: 1     │  ← 1 laptop
└─────────────────┘
```

### Example 3: Kitchen Scene
```
┌─────────────────┐
│ FPS: 25         │
│ Objects: 6      │
│ Frames: 890     │
│ Saved: 3        │
│                 │
│ Current:        │
│   cup: 3        │  ← 3 cups
│   bottle: 2     │  ← 2 bottles
│   person: 1     │  ← 1 person
└─────────────────┘
```

---

## ✨ Visual Benefits

✅ **At-a-glance metrics** - See everything instantly
✅ **Color-coded info** - Easy to distinguish different metrics
✅ **Non-intrusive panel** - Semi-transparent, doesn't block view
✅ **Real-time updates** - All metrics update live
✅ **Object breakdown** - See what's detected right now
✅ **Professional look** - Clean, organized display
✅ **File organization** - Dedicated folder for saves
✅ **Timestamped saves** - Never lose track of when frames were captured

---

**Everything is clearly visible and well-organized! 📊✨**

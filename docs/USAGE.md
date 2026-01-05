# Usage Guide - DrishtiX Ultimate

## Table of Contents
1. [Quick Start](#quick-start)
2. [Detection Modes](#detection-modes)
3. [Dashboard Guide](#dashboard-guide)
4. [Alert Configuration](#alert-configuration)
5. [Model Training](#model-training)
6. [Best Practices](#best-practices)

## Quick Start

### Basic Operation

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Run detection system
python ai_core/drishtix_main.py
```

**Controls:**
- Press `q` - Quit the application
- Press `s` - Take manual screenshot
- Press `a` - Send test alert

### Dashboard Mode

```bash
# Launch web dashboard
streamlit run dashboard1.py
```

Access the dashboard at: **http://localhost:8501**

## Detection Modes

### 1. Real Animal Detection

For actual wildlife monitoring:

```python
# In ai_core/drishtix_main.py
NAME_MAP = {
    "elephant": "ELEPHANT",
    "bear": "WILD BOAR",
    "zebra": "TIGER",
}
```

**Supported Animals:**
- Elephants
- Wild Boars
- Tigers
- Deer
- Bears

### 2. Demo/Testing Mode (Proxy Objects)

For demonstrations without real animals:

```python
NAME_MAP = {
    "cat": "TIGER",         # Show cat → Detects as TIGER
    "dog": "WILD BOAR",     # Show dog → Detects as WILD BOAR
    "horse": "DEER",        # Show horse → Detects as DEER
}
```

**How to Use:**
1. Point camera at common objects (cat, dog pictures)
2. System will treat them as wildlife
3. Perfect for hackathons/demos!

### 3. Custom Detection

Train your own model for specific animals:

```bash
cd training_data
python train.py
```

## Dashboard Guide

### Overview

The Streamlit dashboard provides:
- 📹 Live camera feed with bounding boxes
- 📊 Real-time detection statistics
- 🚨 Alert history log
- 🖼️ Evidence image gallery
- ⚙️ System controls

### Dashboard Features

#### 1. Live Video Feed
- Real-time camera stream
- Bounding boxes around detected animals
- Confidence scores displayed
- FPS counter

#### 2. Control Panel

**Start/Stop Detection**
```python
if st.button("🟢 START DETECTION"):
    # Starts camera and AI processing
    
if st.button("🔴 STOP DETECTION"):
    # Stops system safely
```

**Manual Alert**
```python
if st.button("📤 SEND TEST ALERT"):
    # Sends test notification
```

#### 3. Alert History
```
[2026-01-05 14:30:22] 🐘 ELEPHANT detected! (conf: 0.87)
[2026-01-05 14:25:15] 🐗 WILD BOAR detected! (conf: 0.73)
```

#### 4. Metrics Display
- **Total Detections**: Count of all animals detected
- **Active Alerts**: Current threats in view
- **Last Alert**: Time since last notification
- **System Uptime**: Total running time

### Navigation

```
Sidebar Controls:
├── 📷 Camera Settings
├── 🎯 Detection Threshold
├── ⏱️ Alert Cooldown
├── 🔊 Audio Enable/Disable
└── 📁 View Evidence Folder
```

## Alert Configuration

### WhatsApp Alerts

**Setup:**
1. Configure phone number in `.env`:
   ```env
   WHATSAPP_PHONE=+91XXXXXXXXXX
   ```

2. First-time setup:
   ```bash
   # Login to WhatsApp Web
   # The script will open browser automatically
   ```

**Alert Format:**
```
🚨 WILDLIFE ALERT! 🚨
Animal: ELEPHANT
Confidence: 87%
Time: 2026-01-05 14:30:22
Location: Farm Perimeter

[Image attached]
```

**Customization:**
```python
# In ai_core/whatsapp_sender.py
def send_alert_with_image(phone, animal_name, confidence, image_path):
    message = f"""
    🚨 CUSTOM ALERT 🚨
    Detected: {animal_name}
    Threat Level: {"HIGH" if confidence > 0.7 else "MEDIUM"}
    Action: Check perimeter immediately!
    """
```

### Telegram Alerts

**Setup:**
1. Configure bot in `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=your_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

2. Send test message:
   ```python
   import requests
   
   url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
   requests.post(url, data={
       "chat_id": CHAT_ID,
       "text": "✅ DrishtiX Test Alert"
   })
   ```

### Audio Alerts

**Configure Audio:**
```python
# In dashboard1.py
SIREN_FILE = "alarm.mp3"  # Your audio file

# Play alert
pygame.mixer.music.load(SIREN_FILE)
pygame.mixer.music.play()
```

**Custom Sounds:**
1. Add MP3/WAV file to project root
2. Update `SIREN_FILE` path
3. Adjust volume:
   ```python
   pygame.mixer.music.set_volume(0.7)  # 70% volume
   ```

### Alert Cooldown

Prevent spam alerts:

```python
# In ai_core/drishtix_main.py
ALERT_COOLDOWN = 30  # seconds

if time.time() - last_alert_time > ALERT_COOLDOWN:
    send_alert()
    last_alert_time = time.time()
```

## Model Training

### Prepare Dataset

1. **Collect Images:**
   - Minimum 100 images per class
   - Various angles, lighting conditions
   - Mix of close and far shots

2. **Annotate with Roboflow:**
   - Upload to [roboflow.com](https://roboflow.com)
   - Draw bounding boxes
   - Export in YOLO format

3. **Organize Dataset:**
   ```
   training_data/dataset/
   ├── train/
   │   ├── images/
   │   └── labels/
   ├── valid/
   │   ├── images/
   │   └── labels/
   └── test/
       ├── images/
       └── labels/
   ```

### Train Model

```bash
cd training_data
python train.py
```

**Training Script:**
```python
from ultralytics import YOLO

# Load base model
model = YOLO('yolov8n.pt')

# Train
results = model.train(
    data='dataset/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device='cuda:0'  # or 'cpu'
)

# Evaluate
metrics = model.val()

# Save
model.save('models/best.pt')
```

### Use Custom Model

```python
# In ai_core/drishtix_main.py
MODEL_PATH = "models/best.pt"  # Your trained model
```

## Best Practices

### 1. Camera Placement

✅ **Do:**
- Mount at animal eye level (2-3 feet for most)
- Cover entry/exit points
- Ensure good lighting or use IR camera
- Protect from weather (housing/enclosure)
- Clear field of view

❌ **Don't:**
- Place too high or too low
- Point directly at sun
- Obstruct with vegetation
- Expose to rain without protection

### 2. Detection Optimization

**Adjust Confidence Thresholds:**
```python
# High confidence = fewer false positives, might miss animals
ELEPHANT_THRESHOLD = 0.70  # Very strict

# Low confidence = more detections, more false positives
CAT_PROXY_THRESHOLD = 0.20  # Very sensitive
```

**Frame Confirmation:**
```python
# Require multiple consecutive frames
CONFIRMATION_FRAMES = 5  # Must see 5 frames in a row

# Balance: 3-5 frames for quick response
# 10+ frames for very stable environments
```

### 3. Alert Management

**Smart Cooldown:**
```python
# Per-animal cooldown tracking
last_alerts = {
    "ELEPHANT": 0,
    "TIGER": 0,
    "WILD_BOAR": 0
}

# Different cooldowns per animal
cooldowns = {
    "ELEPHANT": 60,      # 1 minute
    "TIGER": 120,        # 2 minutes (more serious)
    "WILD_BOAR": 30      # 30 seconds
}
```

### 4. Performance Tips

**Optimize FPS:**
```python
# Reduce resolution for faster processing
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Process every Nth frame
frame_count = 0
if frame_count % 2 == 0:  # Process every 2nd frame
    results = model(frame)
```

**GPU Acceleration:**
```python
# Use CUDA if available
model = YOLO('yolov8n.pt')
model.to('cuda')  # Use GPU
```

### 5. Maintenance

**Daily:**
- Check camera feed
- Verify internet connection
- Test alert channels

**Weekly:**
- Review alert logs
- Clean camera lens
- Update detection thresholds if needed

**Monthly:**
- Review false positive rate
- Retrain model with new data
- Update software dependencies

## Advanced Features

### Multi-Camera Setup

```python
# Create multiple detector instances
cameras = [0, 1, 2]  # Multiple camera indices

for cam_id in cameras:
    threading.Thread(
        target=run_detection,
        args=(cam_id,)
    ).start()
```

### Cloud Storage Integration

```python
# Upload to cloud
import boto3

def upload_to_s3(image_path):
    s3 = boto3.client('s3')
    s3.upload_file(
        image_path,
        'wildlife-alerts',
        f'evidence/{timestamp}.jpg'
    )
```

### Scheduled Operation

```python
# Run only during specific hours
import schedule

def job():
    run_detection()

# Run from sunset to sunrise
schedule.every().day.at("18:00").do(job)
schedule.every().day.at("06:00").do(stop_detection)
```

## Troubleshooting

### Low Detection Rate
- Decrease confidence threshold
- Improve lighting
- Clean camera lens
- Retrain with more data

### Too Many False Positives
- Increase confidence threshold
- Increase confirmation frames
- Remove problematic classes from NAME_MAP
- Retrain model with negative examples

### Delayed Alerts
- Check internet connection
- Reduce image size
- Use faster alert method (Telegram > WhatsApp)
- Enable local caching

---

**For more help, see [INSTALLATION.md](INSTALLATION.md) or open an issue on GitHub.**

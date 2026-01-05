# API Documentation - DrishtiX Ultimate

## Table of Contents
1. [Core Modules](#core-modules)
2. [Detection API](#detection-api)
3. [Alert System API](#alert-system-api)
4. [Configuration](#configuration)
5. [Data Structures](#data-structures)

## Core Modules

### drishtix_main.py

Main detection engine with YOLOv8 integration.

#### Classes

##### `ThreatTracker`
Manages detection persistence and noise filtering.

```python
class ThreatTracker:
    """
    Filters out noise and glitches in detections.
    
    Attributes:
        active_threats (dict): Current detected threats and their counts
    """
    
    def __init__(self):
        """Initialize empty threat tracker."""
        
    def update(self, raw_detections: list) -> list:
        """
        Update tracker with new detections.
        
        Args:
            raw_detections: List of (name, confidence, box) tuples
            
        Returns:
            List of confirmed threats that passed filtering
        """
```

**Example Usage:**
```python
tracker = ThreatTracker()
confirmed = tracker.update([
    ("TIGER", 0.85, [100, 100, 200, 200]),
    ("ELEPHANT", 0.92, [300, 150, 450, 300])
])
```

#### Functions

##### `main()`
Main detection loop.

```python
def main():
    """
    Start wildlife detection system.
    
    - Initializes camera and model
    - Runs detection loop
    - Handles alerts
    - Manages cleanup on exit
    """
```

### whatsapp_sender.py

WhatsApp integration module.

#### Functions

##### `send_alert_with_image(phone_no, message, image_path)`

```python
def send_alert_with_image(phone_no: str, message: str, image_path: str) -> bool:
    """
    Send WhatsApp alert with image attachment.
    
    Args:
        phone_no (str): Phone number with country code (e.g., '+919876543210')
        message (str): Alert message text
        image_path (str): Path to image file
        
    Returns:
        bool: True if sent successfully, False otherwise
        
    Raises:
        FileNotFoundError: If image_path doesn't exist
        
    Example:
        >>> send_alert_with_image(
        ...     "+919876543210",
        ...     "🚨 TIGER detected at 14:30",
        ...     "breached/tiger_20260105_143022.jpg"
        ... )
        True
    """
```

## Detection API

### Detection Configuration

```python
# In ai_core/drishtix_main.py

# Model settings
MODEL_PATH = "yolov8n.pt"          # Path to YOLO model
CAMERA_INDEX = 0                   # Camera source

# Detection mapping
NAME_MAP = {
    "cat": "TIGER",                # Map detected class to threat name
    "dog": "WILD BOAR",
    "elephant": "ELEPHANT"
}

# Confidence thresholds per class
CONFIDENCE_THRESHOLDS = {
    "elephant": 0.50,              # Higher = stricter
    "cat": 0.30,
    "dog": 0.30
}

# Tracking parameters
CONFIRMATION_FRAMES = 5            # Consecutive frames needed
PATIENCE_FRAMES = 10               # Remember for N frames if lost
ALERT_COOLDOWN = 30                # Seconds between alerts
```

### Running Detection

#### Command Line
```bash
python ai_core/drishtix_main.py
```

#### Programmatic
```python
from ai_core.drishtix_main import main

# Run detection
main()
```

#### Custom Integration
```python
import cv2
from ultralytics import YOLO

# Load model
model = YOLO('yolov8n.pt')

# Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Run detection
    results = model(frame)
    
    # Process results
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            name = model.names[cls]
            
            # Your custom logic here
            print(f"Detected: {name} ({conf:.2f})")
```

## Alert System API

### WhatsApp Alerts

#### Basic Alert
```python
from ai_core.whatsapp_sender import send_alert_with_image

# Send alert
success = send_alert_with_image(
    phone_no="+919876543210",
    message="🚨 Wildlife Alert! ELEPHANT detected",
    image_path="breached/elephant_001.jpg"
)
```

#### Custom Message Format
```python
from datetime import datetime

animal = "ELEPHANT"
confidence = 0.87
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

message = f"""
🚨 WILDLIFE ALERT 🚨
━━━━━━━━━━━━━━━━━━
Animal: {animal}
Confidence: {confidence*100:.1f}%
Time: {timestamp}
Location: Farm Perimeter

⚠️ Take immediate action!
"""

send_alert_with_image("+919876543210", message, "alert.jpg")
```

### Telegram Alerts

#### Basic Setup
```python
import requests

BOT_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"

def send_telegram_photo(image_path, caption):
    """Send photo via Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': CHAT_ID, 'caption': caption}
        response = requests.post(url, files=files, data=data)
    
    return response.json()
```

#### Example Usage
```python
send_telegram_photo(
    "breached/tiger_001.jpg",
    "🐅 TIGER detected at North Fence\nConfidence: 92%"
)
```

### Audio Alerts

```python
import pygame

# Initialize
pygame.mixer.init()

# Play siren
def play_siren(sound_file="alarm.mp3", volume=1.0):
    """Play audio alert."""
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
```

## Configuration

### Environment Variables

Create `.env` file:
```env
# Communication
WHATSAPP_PHONE=+919876543210
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=123456789

# Camera
CAMERA_INDEX=0

# Detection
CONFIDENCE_THRESHOLD=0.30
CONFIRMATION_FRAMES=5

# Alerts
ALERT_COOLDOWN=30
ENABLE_AUDIO=true
```

### Loading Configuration

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access variables
PHONE = os.getenv('WHATSAPP_PHONE')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CAMERA = int(os.getenv('CAMERA_INDEX', 0))
THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.3))
```

## Data Structures

### Detection Result

```python
# Single detection
detection = {
    'name': 'TIGER',              # Animal name
    'confidence': 0.87,            # Confidence score (0-1)
    'box': [100, 150, 300, 400],  # Bounding box [x1, y1, x2, y2]
    'timestamp': '2026-01-05 14:30:22'
}
```

### Alert Record

```python
# Alert log entry
alert = {
    'animal': 'ELEPHANT',
    'confidence': 0.92,
    'timestamp': '2026-01-05 14:30:22',
    'image_path': 'breached/elephant_20260105_143022.jpg',
    'alert_sent': True,
    'channels': ['whatsapp', 'telegram']
}
```

### Threat Tracker State

```python
# Internal tracker state
tracker_state = {
    'active_threats': {
        'TIGER': 7,        # Frame count
        'ELEPHANT': 12
    },
    'last_alerts': {
        'TIGER': 1704460822,      # Unix timestamp
        'ELEPHANT': 1704460750
    }
}
```

## Advanced Usage

### Custom Detection Pipeline

```python
from ultralytics import YOLO
import cv2

class CustomDetector:
    """Custom wildlife detector with preprocessing."""
    
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        
    def preprocess(self, frame):
        """Apply preprocessing to frame."""
        # Convert to grayscale for better night detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Enhance contrast
        enhanced = cv2.equalizeHist(gray)
        return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
    
    def detect(self, frame, preprocess=True):
        """Run detection with optional preprocessing."""
        if preprocess:
            frame = self.preprocess(frame)
        
        results = self.model(frame)
        detections = []
        
        for result in results:
            for box in result.boxes:
                detections.append({
                    'class': self.model.names[int(box.cls[0])],
                    'confidence': float(box.conf[0]),
                    'bbox': box.xyxy[0].tolist()
                })
        
        return detections

# Usage
detector = CustomDetector()
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
detections = detector.detect(frame)
```

### Multi-Threaded Alert System

```python
import threading
import queue

class AlertManager:
    """Thread-safe alert queue manager."""
    
    def __init__(self):
        self.queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self._process_alerts)
        self.thread.start()
    
    def add_alert(self, animal, image_path):
        """Add alert to queue."""
        self.queue.put((animal, image_path))
    
    def _process_alerts(self):
        """Process alerts from queue."""
        while self.running:
            try:
                animal, image = self.queue.get(timeout=1)
                # Send alerts
                send_alert_with_image(PHONE, f"Alert: {animal}", image)
                self.queue.task_done()
            except queue.Empty:
                continue
    
    def stop(self):
        """Stop alert processing."""
        self.running = False
        self.thread.join()

# Usage
alert_mgr = AlertManager()
alert_mgr.add_alert("TIGER", "tiger.jpg")
```

---

For more examples, see the source code in `ai_core/` directory.

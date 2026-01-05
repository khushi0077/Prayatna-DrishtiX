# Frequently Asked Questions (FAQ)

## General Questions

### What is DrishtiX Ultimate?

DrishtiX Ultimate is an AI-powered wildlife intrusion detection system that uses computer vision (YOLOv8) to detect and alert about wildlife presence in real-time. It's designed to prevent human-wildlife conflicts by providing early warnings.

### Who is this for?

- **Farmers**: Protect crops from wildlife damage
- **Communities**: Safety alerts for wildlife in residential areas
- **Conservation**: Monitor wildlife movement
- **Researchers**: Study animal behavior patterns
- **Security**: Perimeter monitoring

### How much does it cost?

The software is **free and open-source**. Hardware costs:
- Basic setup: $40-60 (camera + ESP32 + sensors)
- Full setup: $150-200 (with weatherproofing, backup power)

## Technical Questions

### What animals can it detect?

**Out of the box:**
- Elephants
- Tigers
- Wild Boars
- Deer
- Bears

**Custom training:** You can train it to detect any animal with enough training images.

### How accurate is the detection?

- **Real animals**: 70-95% accuracy (depends on lighting, distance, model training)
- **False positive rate**: ~5-10% (adjustable via confidence thresholds)
- **Detection range**: 5-15 meters (depends on camera and animal size)

### What hardware do I need?

**Minimum:**
- Computer/Raspberry Pi with Python 3.8+
- USB webcam (720p+)
- Internet connection (for alerts)

**Recommended:**
- Raspberry Pi 4 (4GB RAM) or better
- HD camera (1080p)
- ESP32 + ultrasonic sensor
- Power backup (UPS/power bank)

### Can it work without internet?

**Partially yes:**
- Detection and local alerts work offline
- Bluetooth alerts work offline
- WhatsApp/Telegram alerts need internet
- Can queue alerts and send when internet returns

### Does it work at night?

**Yes, with proper setup:**
- Use IR/night vision camera
- Add IR illuminators
- Adjust confidence thresholds
- May have reduced accuracy vs. daylight

### How fast is the detection?

- **Detection latency**: 100-500ms per frame
- **Alert delay**: 2-10 seconds (includes confirmation frames)
- **FPS**: 10-30 (depends on hardware)

## Installation & Setup

### I'm getting ImportError. What to do?

```bash
# Solution 1: Install missing package
pip install [package_name]

# Solution 2: Reinstall all
pip install -r requirements.txt --force-reinstall

# Solution 3: Check Python version
python --version  # Should be 3.8+
```

### Camera not detected. How to fix?

```bash
# Linux: Check camera devices
ls /dev/video*

# Test camera
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# Try different index
CAMERA_INDEX=1  # in .env file

# Check permissions (Linux)
sudo usermod -a -G video $USER
```

### WhatsApp alerts not working?

**Common fixes:**
1. **Login to WhatsApp Web first** - Open web.whatsapp.com and scan QR
2. **Check phone format** - Must be `+[country code][number]` (e.g., `+919876543210`)
3. **First message** - Send first message manually to create chat
4. **Browser issues** - Update Chrome/browser
5. **Firewall** - Check if port 443 is open

### How to get Telegram bot token?

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create bot
4. Copy the token provided
5. Get your chat ID from `@userinfobot`
6. Add to `.env` file

### Can I use multiple cameras?

**Yes!** Run multiple instances:

```python
# camera1.py
CAMERA_INDEX = 0
python ai_core/drishtix_main.py

# camera2.py
CAMERA_INDEX = 1
python ai_core/drishtix_main.py
```

Or use threading for single process (see API docs).

## Usage & Configuration

### How to reduce false alarms?

1. **Increase confidence threshold:**
   ```python
   CONFIDENCE_THRESHOLD = 0.50  # Higher = fewer false positives
   ```

2. **Increase confirmation frames:**
   ```python
   CONFIRMATION_FRAMES = 10  # Must see 10 frames in a row
   ```

3. **Train custom model** with negative examples

4. **Adjust camera position** to avoid problematic areas

### How to make it more sensitive?

1. **Lower confidence threshold:**
   ```python
   CONFIDENCE_THRESHOLD = 0.20  # Lower = more detections
   ```

2. **Reduce confirmation frames:**
   ```python
   CONFIRMATION_FRAMES = 3  # Faster alerts
   ```

3. **Better lighting** or use IR camera

### Can I customize alert messages?

**Yes!** Edit `ai_core/whatsapp_sender.py`:

```python
message = f"""
🚨 CUSTOM ALERT 🚨
Location: My Farm
Animal: {animal_name}
Time: {timestamp}
Action Required: Check perimeter!
"""
```

### How to change alert cooldown?

```python
# In ai_core/drishtix_main.py
ALERT_COOLDOWN = 60  # seconds between alerts
```

### Can I disable audio alerts?

**In dashboard:**
- Uncheck "Enable Audio" option

**In code:**
```python
# Comment out or set to False
ENABLE_AUDIO = False
```

## Deployment & Maintenance

### How to run 24/7?

**Linux/Raspberry Pi:**

```bash
# Create systemd service
sudo nano /etc/systemd/system/drishtix.service
```

```ini
[Unit]
Description=DrishtiX Wildlife Detection
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/DrishtiX_Ultimate
ExecStart=/home/pi/DrishtiX_Ultimate/.venv/bin/python ai_core/drishtix_main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable drishtix
sudo systemctl start drishtix
```

### How much power does it consume?

- **Raspberry Pi 4**: 5-8W
- **Webcam**: 2-3W
- **ESP32**: 0.5-1W
- **Total**: ~10W (can run on solar)

### How to backup the system?

```bash
# Backup configuration
cp .env .env.backup

# Backup evidence images
tar -czf breached_backup.tar.gz breached/

# Backup custom models
cp ai_core/models/best.pt models_backup/
```

### Storage requirements?

- **Software**: ~500MB
- **Models**: ~50MB per model
- **Images**: ~100KB per detection
- **Estimate**: 10GB for 100,000 detections

### How to update?

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart drishtix
```

## Training & Customization

### How to train for new animals?

1. **Collect images** (100+ per animal)
2. **Annotate** with Roboflow
3. **Export** in YOLO format
4. **Place** in `training_data/dataset/`
5. **Train**:
   ```bash
   cd training_data
   python train.py
   ```
6. **Use** new model in `ai_core/drishtix_main.py`

### How many images do I need?

- **Minimum**: 50 images per class
- **Good**: 100-200 images per class
- **Best**: 500+ images per class
- **Variety**: Different angles, lighting, distances

### Can I use pre-trained models?

**Yes!** Options:
1. Use default YOLOv8 (80 classes including animals)
2. Download wildlife-specific models
3. Fine-tune on your data

### How long does training take?

- **Small dataset (100 images)**: 30 mins - 1 hour
- **Medium dataset (500 images)**: 2-4 hours
- **Large dataset (2000+ images)**: 6-12 hours

*Note: Depends on GPU. CPU training is much slower.*

## Troubleshooting

### Detection is slow/laggy

**Solutions:**
1. Reduce resolution: `640x480` instead of `1920x1080`
2. Lower FPS: `cap.set(cv2.CAP_PROP_FPS, 15)`
3. Use smaller model: `yolov8n.pt` instead of `yolov8x.pt`
4. Use GPU if available
5. Process every Nth frame

### Too many false positives

1. Increase confidence threshold
2. Add more confirmation frames
3. Retrain with negative samples
4. Adjust camera position
5. Use better model (yolov8m/l)

### Alerts not sending

**WhatsApp:**
- Check internet connection
- Verify phone number format
- Login to WhatsApp Web
- Check browser automation working

**Telegram:**
- Verify bot token
- Verify chat ID
- Test with curl:
  ```bash
  curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
       -d "chat_id=<CHAT_ID>&text=Test"
  ```

### System crashes/freezes

1. **Check memory**: `free -h`
2. **Check CPU**: `top`
3. **Reduce load**: Lower resolution, FPS
4. **Add swap**: If low memory
5. **Check logs**: For error messages

## Best Practices

### Camera placement tips?

✅ **Do:**
- Mount 3-4 feet high
- Clear field of view
- Cover entry/exit points
- Protect from weather
- Good lighting or IR

❌ **Don't:**
- Point at sun directly
- Place behind glass (reflections)
- Too high or too low
- Exposed to rain without housing

### Security recommendations?

1. **Change default passwords** on all devices
2. **Use environment variables** for credentials
3. **Keep software updated**
4. **Use VPN** for remote access
5. **Enable firewall**
6. **Regular backups**

### Performance optimization?

```python
# Optimize detection
CONFIDENCE_THRESHOLD = 0.35    # Balance accuracy/speed
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Process every 2nd frame for speed
if frame_count % 2 == 0:
    results = model(frame)
```

## Getting Help

### Still have questions?

1. **Check Documentation:**
   - [README.md](../README.md)
   - [INSTALLATION.md](INSTALLATION.md)
   - [USAGE.md](USAGE.md)
   - [HARDWARE_SETUP.md](HARDWARE_SETUP.md)

2. **Search Issues:** [GitHub Issues](https://github.com/vikrammm24/Prayatna-DrishtiX/issues)

3. **Ask Question:** Open new issue with `question` label

4. **Contact Maintainers:**
   - [@vikrammm24](https://github.com/vikrammm24)
   - [@khushi0077](https://github.com/khushi0077)

### How to contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines!

---

**Don't see your question? [Open an issue](https://github.com/vikrammm24/Prayatna-DrishtiX/issues/new) and we'll add it!**

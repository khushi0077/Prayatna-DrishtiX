# Quick Start Guide - DrishtiX Ultimate

Get up and running in 5 minutes! 🚀

## Prerequisites

- Python 3.8+ installed
- Webcam or camera connected
- Internet connection (for alerts)

## Installation (3 minutes)

### Step 1: Clone and Setup

```bash
# Clone repository
git clone https://github.com/vikrammm24/Prayatna-DrishtiX.git
cd DrishtiX_Ultimate

# Create virtual environment
python -m venv .venv

# Activate (choose your OS)
source .venv/bin/activate          # Linux/Mac
.venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Alerts

```bash
# Copy example config
cp .env.example .env

# Edit with your details
nano .env  # or use any text editor
```

**Minimum configuration:**
```env
WHATSAPP_PHONE=+91XXXXXXXXXX
CAMERA_INDEX=0
```

### Step 3: Test Camera

```bash
python -c "import cv2; cap=cv2.VideoCapture(0); print('✅ Camera OK' if cap.isOpened() else '❌ Error')"
```

## First Run (2 minutes)

### Option 1: Command Line (Simple)

```bash
python ai_core/drishtix_main.py
```

**Controls:**
- Press `q` to quit
- Press `s` for screenshot

### Option 2: Web Dashboard (Recommended)

```bash
streamlit run dashboard1.py
```

**Then open:** http://localhost:8501

## Quick Test

### Demo Mode (No Real Animals Needed!)

The system can detect common objects as wildlife for testing:

```python
# Already configured in the code:
"cat" → Detected as TIGER 🐅
"dog" → Detected as WILD BOAR 🐗  
"horse" → Detected as DEER 🦌
```

**To test:**
1. Start the system
2. Show a picture/toy of a cat to your camera
3. System will alert about "TIGER"! 🎉

## Your First Detection

1. **Start Dashboard:**
   ```bash
   streamlit run dashboard1.py
   ```

2. **Click "🟢 START DETECTION"**

3. **Show test object to camera:**
   - Cat picture → Triggers TIGER alert
   - Dog toy → Triggers WILD BOAR alert

4. **Check Alerts:**
   - Look at dashboard alert log
   - Check WhatsApp for image message
   - Hear audio siren (if enabled)

5. **View Evidence:**
   - Images saved in `breached/` folder
   - Named with timestamp

## Next Steps

### ✅ Working? Congratulations! 

Now you can:

1. **Deploy for Real Use:**
   - Read [USAGE.md](docs/USAGE.md)
   - See [HARDWARE_SETUP.md](docs/HARDWARE_SETUP.md)

2. **Customize Detection:**
   - Adjust confidence thresholds
   - Add more animals
   - Train custom model

3. **Add Sensors:**
   - Setup ESP32 ultrasonic
   - Add multiple cameras

### ❌ Issues? Quick Fixes

**Camera not working:**
```bash
# Try different camera index
CAMERA_INDEX=1  # in .env
```

**ImportError:**
```bash
pip install --upgrade opencv-python ultralytics streamlit
```

**WhatsApp not sending:**
- Login to WhatsApp Web first
- Check phone number format: `+[country][number]`

## Common Commands Cheat Sheet

```bash
# Activate environment
source .venv/bin/activate

# Run detection
python ai_core/drishtix_main.py

# Run dashboard
streamlit run dashboard1.py

# Update dependencies
pip install -r requirements.txt --upgrade

# Check camera
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# View logs
tail -f *.log  # if logs are enabled
```

## File Structure (What's What?)

```
DrishtiX_Ultimate/
├── ai_core/
│   ├── drishtix_main.py      ← Main detection script
│   └── whatsapp_sender.py    ← Alert system
├── dashboard1.py              ← Web interface (start here!)
├── requirements.txt           ← Dependencies list
├── .env                       ← Your config (create from .env.example)
└── breached/                  ← Evidence images saved here
```

## Pro Tips

💡 **Tip 1**: Use dashboard mode - it's much easier than command line!

💡 **Tip 2**: Start with demo mode (cat/dog detection) before deploying for real animals

💡 **Tip 3**: Adjust `CONFIDENCE_THRESHOLD` if too sensitive or not sensitive enough

💡 **Tip 4**: Check `breached/` folder to see captured images

💡 **Tip 5**: Use `ALERT_COOLDOWN` to avoid spam alerts

## Demo for Presentations

**Want to show off the system?**

1. Start dashboard: `streamlit run dashboard1.py`
2. Use your phone to show cat/dog pictures to camera
3. Watch real-time detection and alerts!
4. Perfect for hackathons and demos 🏆

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Camera error | Try `CAMERA_INDEX=1` or check USB connection |
| Import errors | Run `pip install -r requirements.txt` |
| No alerts | Check `.env` file has correct phone number |
| Dashboard won't start | Run `pip install streamlit --upgrade` |
| Low accuracy | Increase confidence threshold in code |

## Getting Help

- **Full docs**: See `docs/` folder
- **Issues**: [GitHub Issues](https://github.com/vikrammm24/Prayatna-DrishtiX/issues)
- **Questions**: Open a discussion on GitHub

---

**That's it! You're ready to detect wildlife! 🦁🐘🐅**

For detailed information, check out the complete documentation in the `docs/` folder.

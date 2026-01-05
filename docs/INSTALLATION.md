# Installation Guide - DrishtiX Ultimate

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Software Installation](#software-installation)
3. [Hardware Setup](#hardware-setup)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+), Windows 10+, macOS 11+
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended)
- **Storage**: 5GB free space
- **Camera**: USB webcam or IP camera
- **Internet**: For cloud alerts (optional for local operation)

### Recommended Requirements
- **CPU**: Intel i5 or equivalent (i7 for better performance)
- **GPU**: NVIDIA GPU with CUDA support (optional, speeds up detection)
- **RAM**: 8GB+
- **Storage**: 10GB+ SSD

## Software Installation

### Step 1: Install Python

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.8 python3-pip python3-venv
```

#### Windows
Download and install from [python.org](https://www.python.org/downloads/)
- ✅ Check "Add Python to PATH" during installation

#### macOS
```bash
brew install python@3.8
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/vikrammm24/Prayatna-DrishtiX.git
cd DrishtiX_Ultimate
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### Step 5: Install System Dependencies

#### Ubuntu/Debian
```bash
# For OpenCV
sudo apt install python3-opencv libopencv-dev

# For audio support
sudo apt install portaudio19-dev python3-pyaudio

# For Bluetooth (optional)
sudo apt install libbluetooth-dev
```

#### macOS
```bash
brew install portaudio
```

#### Windows
Most dependencies are included in the pip packages. For audio:
- Download and install [PyAudio wheel](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

## Hardware Setup

### Camera Setup

#### USB Webcam
1. Connect webcam to USB port
2. Verify camera is detected:
   ```bash
   # Linux
   ls /dev/video*
   
   # Windows - check Device Manager
   
   # Test with Python
   python -c "import cv2; print('Camera OK' if cv2.VideoCapture(0).isOpened() else 'Camera Error')"
   ```

#### IP Camera
1. Configure your IP camera to stream via RTSP
2. Note the RTSP URL format: `rtsp://username:password@ip:port/stream`
3. Update `CAMERA_INDEX` in configuration

### ESP32 Setup (Optional)

1. Install Arduino IDE from [arduino.cc](https://www.arduino.cc/en/software)
2. Add ESP32 board support:
   - Go to File → Preferences
   - Add to "Additional Board Manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
3. Install ESP32 board from Tools → Board → Boards Manager
4. Upload firmware from `firmware/esp32_ultrasonic_guard/`

## Configuration

### Step 1: Create Environment File

```bash
cp .env.example .env
```

### Step 2: Configure Communication

#### WhatsApp Setup
1. Open WhatsApp Web at [web.whatsapp.com](https://web.whatsapp.com)
2. Scan QR code with your phone
3. Update `.env`:
   ```env
   WHATSAPP_PHONE=+91XXXXXXXXXX
   ```

#### Telegram Setup
1. Create a bot with [@BotFather](https://t.me/BotFather):
   - Send `/newbot`
   - Follow instructions
   - Copy the bot token
2. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
3. Update `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=123456789
   ```

### Step 3: Configure Detection Settings

Edit `.env` or directly in `ai_core/drishtix_main.py`:
```python
CAMERA_INDEX = 0  # Your camera index
CONFIDENCE_THRESHOLD = 0.30  # Adjust sensitivity
```

### Step 4: Download Models (if needed)

The repository includes `yolov8n.pt`. For custom models:
```bash
# Download from Ultralytics
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# Or use custom trained model
cp path/to/your/model.pt ai_core/models/best.pt
```

## Verification

### Test Installation

```bash
# 1. Test Python imports
python -c "import cv2, ultralytics, streamlit; print('✅ All imports successful')"

# 2. Test camera
python -c "import cv2; cap = cv2.VideoCapture(0); print('✅ Camera OK' if cap.isOpened() else '❌ Camera Error'); cap.release()"

# 3. Test YOLO model
python -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); print('✅ Model loaded')"
```

### Run Quick Test

```bash
# Test detection without alerts
python ai_core/drishtix_main.py
```
- Press 'q' to quit
- Verify video feed appears
- Check console for detection logs

### Test Dashboard

```bash
streamlit run dashboard1.py
```
- Open browser to http://localhost:8501
- Verify dashboard loads
- Check camera feed

## Troubleshooting

### Common Issues

#### ImportError: No module named 'cv2'
```bash
pip install opencv-python --upgrade
```

#### Camera not detected
```bash
# Linux: Check permissions
sudo usermod -a -G video $USER
# Logout and login again

# Check camera index
python -c "for i in range(5): import cv2; print(f'Camera {i}: {cv2.VideoCapture(i).isOpened()}')"
```

#### CUDA/GPU issues
```bash
# Install CUDA-enabled PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

#### WhatsApp not sending
- Ensure WhatsApp Web is logged in
- Check phone number format: +[country_code][number]
- Verify internet connection
- Try manual send first from WhatsApp Web

#### Streamlit not starting
```bash
# Install streamlit explicitly
pip install streamlit --upgrade

# Clear cache
streamlit cache clear
```

#### Permission denied (Linux)
```bash
# For camera
sudo chmod 666 /dev/video0

# For serial (ESP32)
sudo chmod 666 /dev/ttyUSB0
sudo usermod -a -G dialout $USER
```

### Getting Help

1. Check logs in console output
2. Enable debug mode in `.env`:
   ```env
   DEBUG=true
   LOG_LEVEL=DEBUG
   ```
3. Open an issue on GitHub with:
   - Error message
   - System info (`python --version`, OS)
   - Steps to reproduce

## Next Steps

After successful installation:
1. ✅ Read [USAGE.md](USAGE.md) for operation guide
2. ✅ See [HARDWARE_SETUP.md](HARDWARE_SETUP.md) for sensor integration
3. ✅ Check [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute

---

**Installation complete! 🎉 You're ready to detect wildlife.**

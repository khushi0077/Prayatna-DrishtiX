Drive Link: https://drive.google.com/drive/folders/1M5h5oQ4DRanghkE-CQkc1i0-0cunvcFI?usp=sharing
# 🐘 DrishtiX Ultimate - AI-Powered Wildlife Intrusion Detection System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple.svg)](https://github.com/ultralytics/ultralytics)

> **An intelligent real-time wildlife detection and alert system to prevent human-wildlife conflicts using computer vision, IoT sensors, and instant communication.**

![DrishtiX Banner](https://img.shields.io/badge/Status-Active-success)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Hardware Setup](#hardware-setup)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Team](#team)

## 🎯 Overview

DrishtiX Ultimate is an advanced AI-powered wildlife intrusion detection system designed to protect agricultural areas, villages, and sensitive zones from wildlife intrusions. The system uses YOLOv8 computer vision models combined with IoT sensors (ESP32 + Ultrasonic) to detect and alert about wildlife presence in real-time.

### Problem Statement
Human-wildlife conflicts cause:
- Loss of crops and property
- Risk to human lives
- Harm to endangered wildlife
- Economic losses for farmers

### Our Solution
An intelligent, non-invasive early warning system that:
- Detects wildlife using AI vision and proximity sensors
- Sends instant alerts via WhatsApp and Telegram
- Provides visual evidence with captured images
- Operates 24/7 with minimal human intervention
- Includes offline Bluetooth alerts for network-scarce areas

## ✨ Features

### 🤖 AI-Powered Detection
- **YOLOv8 Object Detection**: Custom-trained model for wildlife identification
- **Multi-Animal Recognition**: Detects elephants, tigers, wild boars, deer, and more
- **Proxy Object Detection**: Demo mode using common objects (cat → tiger, dog → wild boar)
- **Noise Filtering**: Confirmation frames to prevent false alarms
- **Threat Tracking**: Persistent tracking with memory to avoid duplicate alerts

### 📱 Multi-Channel Alerts
- **WhatsApp Integration**: Instant image alerts with animal details
- **Telegram Notifications**: Backup alert channel with photos
- **Bluetooth/Offline Mode**: Local alerts when internet is unavailable
- **Audio Sirens**: Local warning system with pygame audio

### 📊 Real-Time Dashboard
- **Streamlit Web Interface**: Live camera feed visualization
- **Alert History**: Comprehensive log of all detections
- **Evidence Storage**: Automatic image archiving with timestamps
- **System Metrics**: Detection counts, confidence scores, alert status

### 🔧 Hardware Integration
- **ESP32 Microcontroller**: Ultrasonic proximity detection
- **Multi-Sensor Fusion**: Camera + ultrasonic for robust detection
- **Low Power Design**: Optimized for field deployment

### 📈 Training & Customization
- **Custom Dataset**: Roboflow-based wildlife dataset
- **Fine-Tuned Models**: Optimized for specific regions
- **Easy Retraining**: Scripts included for model updates

## 🏗️ System Architecture

```
┌─────────────────┐
│  Camera Input   │
│   (OpenCV)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  YOLOv8 Model   │◄─────┤  Custom Dataset  │
│   Detection     │      │  (3 classes)     │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│ Threat Tracker  │
│ (Noise Filter)  │
└────────┬────────┘
         │
         ├──────────────┬──────────────┬──────────────┐
         ▼              ▼              ▼              ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ WhatsApp │  │ Telegram │  │Bluetooth │  │  Siren   │
   │  Alert   │  │  Alert   │  │  Alert   │  │  Audio   │
   └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam or IP camera
- WhatsApp account (for alerts)
- Internet connection (for cloud alerts)

### Installation

```bash
# Clone the repository
git clone https://github.com/vikrammm24/Prayatna-DrishtiX.git
cd DrishtiX_Ultimate

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download YOLOv8 model (if not included)
# The yolov8n.pt model is already in the repo
```

### Basic Usage

```bash
# Run the detection system
python ai_core/drishtix_main.py

# Or launch the web dashboard
streamlit run dashboard1.py
```

## 📦 Installation

For detailed installation instructions, see [docs/INSTALLATION.md](docs/INSTALLATION.md)

### Quick Install

```bash
pip install -r requirements.txt
```

### Configuration

Create a configuration file or use environment variables:

```python
# WhatsApp
TARGET_PHONE = "+91XXXXXXXXXX"

# Telegram
BOT_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"

# Camera
CAMERA_INDEX = 0  # 0 for default webcam
```

## 🎮 Usage

### Command Line Mode
```bash
python ai_core/drishtix_main.py
```
- Press 'q' to quit
- Press 's' to take manual screenshot

### Dashboard Mode
```bash
streamlit run dashboard1.py
```
- Access at http://localhost:8501
- View live feed and alerts in real-time
- Monitor detection history

### Training Custom Models
```bash
cd training_data
python train.py
```

For detailed usage instructions, see [docs/USAGE.md](docs/USAGE.md)

## 🔌 Hardware Setup

### Components Required
- ESP32 Development Board
- HC-SR04 Ultrasonic Sensor
- USB Webcam or Raspberry Pi Camera
- Power Supply (5V 2A)
- Connecting Wires

### Wiring Diagram
See [docs/HARDWARE_SETUP.md](docs/HARDWARE_SETUP.md) for detailed instructions.

### ESP32 Configuration
Upload the Arduino sketch from `firmware/esp32_ultrasonic_guard/` to your ESP32.

## 📁 Project Structure

```
DrishtiX_Ultimate/
├── ai_core/                    # Core AI detection modules
│   ├── drishtix_main.py       # Main detection script
│   ├── whatsapp_sender.py     # WhatsApp alert system
│   ├── aggression_tracker.py  # Advanced threat tracking
│   └── models/                # Trained model files
│       └── best.pt
├── firmware/                   # ESP32 Arduino code
│   └── esp32_ultrasonic_guard/
├── training_data/              # Dataset and training scripts
│   ├── train.py
│   ├── dataset/
│   │   ├── train/
│   │   ├── valid/
│   │   └── test/
│   └── data.yaml
├── offline_comms/              # Bluetooth/offline alerts
│   ├── bluetooth_alert.py
│   └── offline_comm.py
├── docs/                       # Documentation
├── breached/                   # Stored alert images
├── dashboard.py                # Streamlit dashboard
├── dashboard1.py               # Enhanced dashboard
├── requirements.txt            # Python dependencies
├── CONTRIBUTING.md            # Contribution guidelines
└── README.md                  # This file
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file:
```env
WHATSAPP_PHONE=+91XXXXXXXXXX
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
CAMERA_INDEX=0
CONFIDENCE_THRESHOLD=0.30
```

### Detection Thresholds
Adjust in `ai_core/drishtix_main.py`:
```python
CONFIDENCE_THRESHOLDS = {
    "elephant": 0.50,
    "tiger": 0.30,
    "wild boar": 0.30
}
CONFIRMATION_FRAMES = 5  # Frames needed to confirm
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black ai_core/
ruff check .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**Prayatna-DrishtiX Development Team**

- **Vikram** - [@vikrammm24](https://github.com/vikrammm24)
- **Harini** - [@khushi0077](https://github.com/khushi0077)

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- Roboflow for dataset management
- Open-source community

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/vikrammm24/Prayatna-DrishtiX/issues)
- Contact maintainers directly

## 🔮 Future Enhancements

- [ ] Mobile app for alerts
- [ ] Multi-camera support
- [ ] Cloud dashboard
- [ ] GPS location tracking
- [ ] Solar power integration
- [ ] Edge AI deployment (Jetson Nano)
- [ ] Thermal camera integration

---

**Made with ❤️ for wildlife conservation and community safety**
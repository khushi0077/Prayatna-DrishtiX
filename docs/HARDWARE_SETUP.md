# Hardware Setup Guide - DrishtiX Ultimate

## Table of Contents
1. [Overview](#overview)
2. [Components Required](#components-required)
3. [ESP32 Ultrasonic Setup](#esp32-ultrasonic-setup)
4. [Camera Setup](#camera-setup)
5. [Power Supply](#power-supply)
6. [Field Deployment](#field-deployment)
7. [Wiring Diagrams](#wiring-diagrams)
8. [Troubleshooting](#troubleshooting)

## Overview

DrishtiX Ultimate uses a dual-sensor approach:
- **Camera (Primary)**: AI-based visual detection using YOLOv8
- **Ultrasonic Sensor (Secondary)**: Proximity detection for backup/trigger

This redundancy ensures reliable detection even in low-light conditions or when visual detection is challenging.

## Components Required

### Essential Components

| Component | Specification | Quantity | Approx. Cost |
|-----------|--------------|----------|--------------|
| ESP32 DevKit | ESP32-WROOM-32 | 1 | $8-10 |
| Ultrasonic Sensor | HC-SR04 | 1-4 | $2-3 each |
| USB Webcam | 720p+ resolution | 1 | $15-30 |
| Power Supply | 5V 2A USB | 1 | $5-8 |
| Jumper Wires | Male-Female | 10 | $3 |
| Breadboard | Standard | 1 | $3 |
| USB Cable | Micro-USB or USB-C | 2 | $5 |

### Optional Components

| Component | Purpose | Cost |
|-----------|---------|------|
| Raspberry Pi Camera | Better integration | $25 |
| Solar Panel (5V) | Off-grid power | $20-40 |
| Power Bank (20000mAh) | Backup power | $25 |
| Weatherproof Enclosure | Outdoor protection | $15-30 |
| PIR Motion Sensor | Additional trigger | $3 |
| Buzzer Module | Local audio alert | $2 |
| LED Indicators | Status display | $5 |

**Total Cost (Essential):** ~$40-60  
**Total Cost (Full Setup):** ~$150-200

## ESP32 Ultrasonic Setup

### Component Overview

**ESP32 Features:**
- Dual-core processor
- WiFi + Bluetooth
- Multiple GPIO pins
- Low power consumption
- Arduino compatible

**HC-SR04 Ultrasonic Sensor:**
- Range: 2cm - 400cm
- Accuracy: ±3mm
- Trigger distance: Configurable
- Power: 5V DC

### Wiring Diagram

```
ESP32                HC-SR04
=====                =======
VIN (5V)    ------>  VCC
GND         ------>  GND
GPIO 5      ------>  TRIG
GPIO 18     ------>  ECHO
```

**Pin Configuration:**
```cpp
#define TRIG_PIN 5
#define ECHO_PIN 18
#define BUZZER_PIN 19  // Optional local buzzer
#define LED_PIN 2      // Built-in LED for status
```

### Physical Assembly

1. **Mount Ultrasonic Sensor:**
   - Place on breadboard or mount directly
   - Ensure sensors face outward (parallel)
   - Height: 1-2 feet from ground
   - Angle: Slight downward tilt (10-15°)

2. **Connect to ESP32:**
   ```
   HC-SR04 VCC  → ESP32 VIN (5V)
   HC-SR04 GND  → ESP32 GND
   HC-SR04 TRIG → ESP32 GPIO 5
   HC-SR04 ECHO → ESP32 GPIO 18
   ```

3. **Optional Components:**
   ```
   Buzzer (+)   → ESP32 GPIO 19
   Buzzer (-)   → ESP32 GND
   LED (+)      → ESP32 GPIO 2 (via 220Ω resistor)
   LED (-)      → ESP32 GND
   ```

### Software Setup

#### 1. Install Arduino IDE

Download from: [arduino.cc/en/software](https://www.arduino.cc/en/software)

#### 2. Add ESP32 Board Support

1. Open Arduino IDE
2. Go to **File → Preferences**
3. Add to "Additional Board Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Go to **Tools → Board → Boards Manager**
5. Search "ESP32" and install

#### 3. Upload Firmware

1. Open `firmware/esp32_ultrasonic_guard/esp32_ultrasonic_guard.ino`
2. Select board: **Tools → Board → ESP32 Dev Module**
3. Select port: **Tools → Port → /dev/ttyUSB0** (or COM port on Windows)
4. Click **Upload** button

#### 4. Verify Operation

Open Serial Monitor (Tools → Serial Monitor):
```
ESP32 Ultrasonic Guard - Started
Distance: 234 cm - CLEAR
Distance: 156 cm - CLEAR
Distance: 45 cm - ALERT!
Distance: 32 cm - ALERT!
```

## Camera Setup

### USB Webcam Setup

#### 1. Connect Camera
- Plug USB webcam into computer/Raspberry Pi
- Check LED indicator (should light up)

#### 2. Test Camera

**Linux:**
```bash
# List cameras
ls -l /dev/video*

# Test with ffmpeg
ffplay /dev/video0

# Test with Python
python -c "import cv2; cap=cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"
```

**Windows:**
```bash
# Check Device Manager → Cameras
# Test with Camera app
```

#### 3. Optimize Settings

```python
import cv2

cap = cv2.VideoCapture(0)

# Set resolution (balance quality vs performance)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Set FPS
cap.set(cv2.CAP_PROP_FPS, 30)

# Adjust brightness (0-255)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)

# Adjust contrast
cap.set(cv2.CAP_PROP_CONTRAST, 128)
```

### IP Camera Setup

#### 1. Configure Camera
- Set static IP address
- Enable RTSP streaming
- Note credentials

#### 2. Get RTSP URL

Common formats:
```
# Generic
rtsp://username:password@192.168.1.100:554/stream

# Hikvision
rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101

# Dahua
rtsp://admin:password@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0

# TP-Link
rtsp://admin:password@192.168.1.100:554/stream1
```

#### 3. Test Stream

```bash
# Using ffplay
ffplay rtsp://username:password@192.168.1.100:554/stream

# Using VLC
vlc rtsp://username:password@192.168.1.100:554/stream
```

#### 4. Use in DrishtiX

```python
# In ai_core/drishtix_main.py
CAMERA_INDEX = "rtsp://admin:password@192.168.1.100:554/stream"
```

### Raspberry Pi Camera Setup

#### 1. Enable Camera
```bash
sudo raspi-config
# Interface Options → Camera → Enable
```

#### 2. Test Camera
```bash
# Capture test image
raspistill -o test.jpg

# Record video
raspivid -o test.h264 -t 10000
```

#### 3. Use with OpenCV
```python
cap = cv2.VideoCapture(0)
# Or use picamera library for better control
```

## Power Supply

### Main System Power

**For Computer/Laptop:**
- Standard AC power
- UPS recommended for power backup

**For Raspberry Pi:**
- 5V 3A power supply (USB-C)
- Recommended: Official Raspberry Pi Power Supply

**For ESP32:**
- 5V 1A minimum
- Can be powered from:
  - USB port of main computer
  - Separate 5V adapter
  - Power bank

### Battery Backup Solutions

#### Option 1: UPS (Uninterruptible Power Supply)
```
Best for: Home/Farm installations
Capacity: 600-1000VA
Runtime: 30-60 minutes
Cost: $50-150
```

#### Option 2: Power Bank
```
Best for: Portable/testing setups
Capacity: 20000mAh
Runtime: 8-12 hours (Raspberry Pi + ESP32)
Cost: $25-40
```

#### Option 3: Solar Power
```
Best for: Remote field deployment
Solar Panel: 20W 5V
Battery: 12V 7Ah with regulator
Runtime: Indefinite (with sun)
Cost: $60-100
```

### Solar Setup Diagram

```
Solar Panel (20W)
      ↓
Charge Controller (PWM/MPPT)
      ↓
12V Battery (7Ah)
      ↓
DC-DC Converter (12V → 5V)
      ↓
USB Hub
      ├→ Raspberry Pi/Computer
      └→ ESP32
```

## Field Deployment

### Installation Checklist

#### Pre-Installation
- [ ] All components tested individually
- [ ] Software configured and tested
- [ ] Alert systems verified
- [ ] Power supply ready
- [ ] Weatherproof enclosure obtained
- [ ] Mounting hardware prepared

#### Site Survey
- [ ] Identify animal entry points
- [ ] Check cellular/WiFi coverage
- [ ] Measure available space
- [ ] Note lighting conditions
- [ ] Check power outlet locations
- [ ] Plan camera angles

#### Installation Steps

1. **Mount Enclosure:**
   - Height: 3-4 feet from ground
   - Location: Clear view of entry point
   - Orientation: Protected from rain
   - Stability: Secure to post/wall

2. **Install Camera:**
   - Position inside enclosure
   - Clear acrylic/glass window
   - Angled downward 15-20°
   - Field of view: 10-15 meters

3. **Position Sensors:**
   - Ultrasonic: Facing entry path
   - Distance: 5-10 meters coverage
   - Multiple sensors: 120° spacing

4. **Power Connection:**
   - Main power to enclosure
   - Cable management
   - Waterproof connections
   - Backup battery inside

5. **System Startup:**
   ```bash
   # SSH into system
   ssh pi@192.168.1.100
   
   # Navigate to project
   cd ~/DrishtiX_Ultimate
   
   # Start detection
   python ai_core/drishtix_main.py
   ```

6. **Test Detection:**
   - Walk through detection zone
   - Verify alerts received
   - Check image quality
   - Adjust camera angle if needed

### Weatherproofing

**Enclosure Requirements:**
- IP65 or higher rating
- Transparent front panel (for camera)
- Cable glands for wires
- Ventilation holes (with mesh)

**Recommended Enclosures:**
- Plastic junction box (8"x6"x4")
- DIY PVC pipe housing
- Commercial outdoor camera housing

**Sealing:**
```
- Silicone sealant around edges
- Cable glands with rubber gaskets
- Desiccant packets inside (prevent condensation)
- Ventilation holes covered with fine mesh
```

## Wiring Diagrams

### Basic Setup
```
┌─────────────────────────────────────┐
│         Weatherproof Enclosure       │
│  ┌──────────┐      ┌─────────────┐ │
│  │          │      │             │ │
│  │  ESP32   │◄─────┤ Ultrasonic  │─┼─→ Detection Zone
│  │          │      │   HC-SR04   │ │
│  └────┬─────┘      └─────────────┘ │
│       │                             │
│       │ Serial (USB)                │
└───────┼─────────────────────────────┘
        │
        ▼
┌──────────────┐
│  Main System │
│  (Computer/  │     ┌─────────┐
│  RaspberryPi)│◄────┤ Webcam  │
│              │     └─────────┘
└──────────────┘
```

### Multi-Sensor Setup
```
         Sensor 1 (Front)
              │
              ▼
        ┌─────────┐
    ┌───┤  ESP32  │───┐
    │   └─────────┘   │
    ▼                 ▼
Sensor 2         Sensor 3
(Left)           (Right)

Coverage: 270° arc
Range: 10m per sensor
```

## Troubleshooting

### ESP32 Issues

**Upload Failed:**
```bash
# Hold BOOT button while uploading
# Or add to code:
pinMode(0, INPUT_PULLUP);  # BOOT button as input
```

**Serial Not Detected:**
```bash
# Linux: Check permissions
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/ttyUSB0

# Install drivers (Windows)
# Download from: silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers
```

**Incorrect Readings:**
```cpp
// Add delay between readings
delay(100);

// Check wiring
// Verify 5V power supply
```

### Camera Issues

**No Image:**
- Check USB connection
- Try different USB port
- Verify camera index in code
- Check permissions (Linux)

**Poor Quality:**
- Clean lens
- Adjust lighting
- Increase resolution
- Adjust camera settings

**Lag/Freezing:**
- Reduce resolution
- Lower FPS
- Check CPU usage
- Upgrade to faster computer

### Power Issues

**ESP32 Resets:**
- Insufficient power supply
- Use dedicated 5V 1A adapter
- Check USB cable quality

**System Crashes:**
- Overheating (add cooling)
- Power fluctuations (use UPS)
- Memory issues (restart daily)

## Maintenance

### Daily
- Check system status
- Verify alerts working
- Review detection logs

### Weekly
- Clean camera lens
- Check cable connections
- Test backup power
- Clear old images

### Monthly
- Inspect weatherproofing
- Check sensor alignment
- Update software
- Backup configuration

---

**For software setup, see [INSTALLATION.md](INSTALLATION.md)**  
**For operation guide, see [USAGE.md](USAGE.md)**

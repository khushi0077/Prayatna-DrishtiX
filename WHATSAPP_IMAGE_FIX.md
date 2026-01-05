# WhatsApp Image Sending Fix

## Problem Fixed
The system was sending WhatsApp alert messages but **not including the captured images** of detected animals.

## Solution Implemented

### 1. Created New WhatsApp Sender Module
- **File**: [ai_core/whatsapp_sender.py](ai_core/whatsapp_sender.py)
- Implements two methods for sending images:
  - **Clipboard Method** (Primary): Copies image to clipboard, then pastes in WhatsApp
  - **File Dialog Method** (Fallback): Uses file picker dialog to select and send image

### 2. Updated Dashboard
- **File**: [dashboard.py](dashboard.py)
- Now uses `send_alert_with_image()` function from the new module
- Automatically saves evidence image when threat is detected
- Sends image along with alert message

### 3. Updated AI Core
- **File**: [ai_core/drishtix_main.py](ai_core/drishtix_main.py)
- Captures and saves frame when animal is detected
- Sends both message and image to user

## How It Works

1. **Animal Detection**: When an animal is detected with sufficient confidence
2. **Image Capture**: The current frame is saved as `alert_evidence.jpg` or `threat_evidence.jpg`
3. **WhatsApp Alert**: The system:
   - Copies the image to system clipboard (using `wl-copy` for Wayland or `xclip` for X11)
   - Opens WhatsApp Web with the alert message
   - Pastes the image from clipboard
   - Sends the message with the attached image

## Dependencies Required

Make sure these are installed on your Linux system:

```bash
# For Wayland (Fedora, Ubuntu 22.04+)
sudo dnf install wl-clipboard  # Fedora
sudo apt install wl-clipboard  # Ubuntu

# For X11 (fallback)
sudo dnf install xclip  # Fedora
sudo apt install xclip  # Ubuntu
```

Python packages (already in your code):
- `pywhatkit`
- `pyautogui`
- `opencv-python` (cv2)

## Usage

The fix is automatic! Just run your dashboard or main script:

```bash
# For Dashboard
streamlit run dashboard.py

# For Standalone System
python ai_core/drishtix_main.py
```

## Troubleshooting

### If images still don't send:

1. **Check clipboard tools are installed**:
   ```bash
   which wl-copy  # Should show path if installed
   which xclip    # Fallback option
   ```

2. **Verify image is being saved**:
   - Look for `alert_evidence.jpg` in the main directory
   - Check file permissions

3. **WhatsApp Web issues**:
   - Make sure you're logged into WhatsApp Web in your default browser
   - Check browser allows file system access
   - Try increasing `wait_time` parameter if page loads slowly

4. **Timing adjustments**:
   - If automation is too fast/slow, adjust `time.sleep()` values in `whatsapp_sender.py`
   - Current timings are optimized for average internet speeds

## Technical Details

### Image Sending Flow

```
Threat Detected
    ↓
Save Frame as JPG
    ↓
Copy to Clipboard (wl-copy/xclip)
    ↓
Open WhatsApp Web
    ↓
Paste Image (Ctrl+V)
    ↓
Send Message (Enter)
```

### Key Functions

- `send_alert_with_image(phone_no, animal_name, image_path)`: Main entry point
- `send_whatsapp_with_image_v2()`: Clipboard-based sending (preferred)
- `send_whatsapp_with_image()`: File dialog based sending (fallback)
- `_copy_image_to_clipboard()`: Linux clipboard integration

## Notes

- Images are sent with captions like: "🚨 THREAT DETECTED: [ANIMAL] has breached the perimeter!"
- Alert cooldown prevents spam (60 seconds by default)
- Background threading prevents video feed from freezing during send
- Automatic fallback between clipboard and file dialog methods

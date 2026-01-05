#!/usr/bin/env python3
"""
Test script to verify WhatsApp image sending functionality.
Run this to test before running the full dashboard.
"""

import os
import sys
import cv2
import numpy as np
from datetime import datetime

# Add ai_core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai_core'))

from whatsapp_sender import send_alert_with_image

# Configuration
PHONE_NUMBER = "+918100661171"  # Your phone number
TEST_ANIMAL = "TIGER"

def create_test_image():
    """Create a test image if we don't have one"""
    # Create breached folder
    os.makedirs("breached", exist_ok=True)
    
    # Check if there's already an image in breached folder
    existing_images = [f for f in os.listdir("breached") if f.endswith('.jpg')]
    
    if existing_images:
        # Use existing image
        test_image_path = os.path.join("breached", existing_images[0])
        print(f"✅ Using existing image: {test_image_path}")
        return test_image_path
    
    # Create a simple test image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add colored rectangle
    cv2.rectangle(img, (100, 100), (540, 380), (0, 0, 255), -1)
    
    # Add text
    text = f"TEST BREACH - {TEST_ANIMAL}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (150, 250), font, 1, (255, 255, 255), 2)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cv2.putText(img, timestamp, (200, 300), font, 0.7, (255, 255, 255), 2)
    
    # Save test image
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_image_path = f"breached/TEST_{TEST_ANIMAL}_{timestamp_str}.jpg"
    cv2.imwrite(test_image_path, img)
    
    print(f"✅ Created test image: {test_image_path}")
    return test_image_path

def main():
    print("=" * 70)
    print("WhatsApp Image Sending Test")
    print("=" * 70)
    print()
    print(f"Phone Number: {PHONE_NUMBER}")
    print(f"Test Animal: {TEST_ANIMAL}")
    print()
    
    # Create/get test image
    test_image = create_test_image()
    
    # Verify image exists
    if not os.path.exists(test_image):
        print(f"❌ ERROR: Test image not found: {test_image}")
        return
    
    print(f"📸 Image file: {test_image}")
    print(f"📏 Image size: {os.path.getsize(test_image)} bytes")
    print()
    
    # Ask user to confirm
    print("⚠️  IMPORTANT NOTES:")
    print("1. Make sure you're logged into WhatsApp Web in your default browser")
    print("2. Keep the browser window visible during the test")
    print("3. Don't move your mouse for ~20 seconds after starting")
    print("4. The script will control your mouse and keyboard")
    print()
    
    response = input("Ready to send test message? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("❌ Test cancelled.")
        return
    
    print()
    print("🚀 Starting WhatsApp send test in 3 seconds...")
    print("   Position your browser window if needed...")
    import time
    time.sleep(3)
    
    print()
    print("=" * 70)
    print("SENDING...")
    print("=" * 70)
    
    # Send the test message
    success = send_alert_with_image(PHONE_NUMBER, TEST_ANIMAL, test_image)
    
    print()
    print("=" * 70)
    if success:
        print("✅✅✅ TEST SUCCESSFUL! ✅✅✅")
        print("Check your WhatsApp to verify the image was received.")
    else:
        print("❌❌❌ TEST FAILED! ❌❌❌")
        print("Check the error messages above for details.")
        print()
        print("Troubleshooting tips:")
        print("1. Make sure wl-clipboard is installed: sudo dnf install wl-clipboard")
        print("2. Make sure WhatsApp Web is logged in")
        print("3. Try increasing wait times in whatsapp_sender.py")
        print("4. Check terminal output for specific error messages")
    print("=" * 70)

if __name__ == "__main__":
    main()

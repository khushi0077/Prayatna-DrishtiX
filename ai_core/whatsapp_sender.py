import pywhatkit
import time
import pyautogui as pg
import logging
import os
import subprocess

logging.basicConfig(level=logging.INFO)

def send_whatsapp_with_image_v3(phone_no, message, image_path):
    """
    Most reliable method - uses selenium-style approach with pyautogui.
    Opens WhatsApp, waits properly, pastes image, adds caption.
    
    Args:
        phone_no (str): Phone number with country code
        message (str): Caption text
        image_path (str): Path to image file
    
    Returns:
        bool: Success status
    """
    try:
        if not os.path.exists(image_path):
            logging.error(f"❌ Image not found: {image_path}")
            return False
        
        logging.info(f"🚀 [V3 Method] Sending WhatsApp with image...")
        
        # Step 1: Copy image to clipboard FIRST
        if not _copy_image_to_clipboard(image_path):
            logging.error("❌ Failed to copy image to clipboard")
            return False
        
        logging.info("✅ Image in clipboard, opening WhatsApp...")
        
        # Step 2: Open WhatsApp Web with empty message
        import webbrowser
        wa_url = f"https://web.whatsapp.com/send?phone={phone_no.replace('+', '')}"
        webbrowser.open(wa_url)
        
        logging.info("⏳ Waiting 15 seconds for WhatsApp Web to load...")
        time.sleep(15)  # Give time to load and QR code login if needed
        
        # Step 3: Click on the message input area
        logging.info("🖱️ Clicking message input area...")
        pg.click(700, 900)  # Click in message area (adjust if needed)
        time.sleep(1)
        
        # Step 4: Paste the image
        logging.info("📋 Pasting image...")
        pg.hotkey('ctrl', 'v')
        time.sleep(5)  # Wait for image preview to appear
        
        # Step 5: Type the caption
        logging.info("✍️ Adding caption...")
        time.sleep(1)
        pg.write(message, interval=0.03)
        time.sleep(2)
        
        # Step 6: Send (press Enter)
        logging.info("📤 Sending...")
        pg.press('enter')
        time.sleep(3)
        
        logging.info("✅ Message sent successfully!")
        return True
        
    except Exception as e:
        logging.error(f"❌ Error in v3 method: {e}")
        import traceback
        traceback.print_exc()
        return False

def send_whatsapp_with_image(phone_no, message, image_path, wait_time=15):
    """
    Sends a WhatsApp message with an image attachment using attachment button.
    
    Args:
        phone_no (str): Phone number with country code (e.g., "+918100661171")
        message (str): Caption/message text
        image_path (str): Absolute path to the image file
        wait_time (int): Time to wait for WhatsApp Web to load
    
    Returns:
        bool: True if successful, False otherwise
    """
    import subprocess
    
    try:
        # Validate image exists
        if not os.path.exists(image_path):
            logging.error(f"❌ Image not found: {image_path}")
            return False
        
        logging.info(f"🚀 Sending WhatsApp alert with image to {phone_no}...")
        
        # Step 1: Copy image to clipboard first (as backup)
        _copy_image_to_clipboard(image_path)
        
        # Step 2: Open WhatsApp Web chat (without message initially)
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone_no,
            message=".",  # Send minimal text first
            wait_time=wait_time,
            tab_close=False,
            close_time=2
        )
        
        logging.info("✅ WhatsApp Web opened, waiting for page to load...")
        time.sleep(8)  # Give extra time for the page to fully load
        
        # Step 3: Clear the dot we sent
        pg.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pg.press('backspace')
        time.sleep(0.5)
        
        # Step 4: Paste image from clipboard
        logging.info("📋 Pasting image from clipboard...")
        pg.hotkey('ctrl', 'v')
        time.sleep(4)  # Wait for image preview to appear
        
        # Step 5: Add caption
        logging.info("✍️ Adding caption...")
        pg.write(message, interval=0.02)
        time.sleep(1)
        
        # Step 6: Send the image
        logging.info("📤 Sending image...")
        pg.press('enter')
        time.sleep(3)
        
        logging.info("✅ WhatsApp alert with image sent successfully!")
        
        # Optional: Close the tab
        time.sleep(1)
        pg.hotkey('ctrl', 'w')
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Failed to send WhatsApp message: {e}")
        return False


def send_whatsapp_with_image_v2(phone_no, message, image_path):
    """
    Alternative method using clipboard for more reliable image sending.
    Works better on Linux systems.
    
    Args:
        phone_no (str): Phone number with country code
        message (str): Caption text
        image_path (str): Path to image file
    
    Returns:
        bool: Success status
    """
    import subprocess
    
    try:
        if not os.path.exists(image_path):
            logging.error(f"❌ Image not found: {image_path}")
            return False
        
        logging.info(f"🚀 Sending WhatsApp with image (clipboard method)...")
        
        # Step 1: Copy image to clipboard FIRST
        success = _copy_image_to_clipboard(image_path)
        if not success:
            logging.error("❌ Failed to copy image to clipboard")
            return False
        
        logging.info("✅ Image copied to clipboard, opening WhatsApp...")
        
        # Step 2: Open WhatsApp chat (message will be typed)
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone_no,
            message=message,
            wait_time=18,  # Increased wait time for stability
            tab_close=False
        )
        
        logging.info("⏳ Waiting for message to be typed and chat to be ready...")
        time.sleep(8)  # Wait longer for the message to be fully typed
        
        # Step 3: Clear the text field and paste image
        logging.info("🧹 Clearing text field...")
        pg.hotkey('ctrl', 'a')  # Select all text
        time.sleep(0.5)
        
        # Step 4: Paste image from clipboard (this will replace the text)
        logging.info("📋 Pasting image from clipboard...")
        pg.hotkey('ctrl', 'v')
        time.sleep(4)  # Wait for image to load in the chat
        
        # Step 5: Re-type the message as caption (since we cleared it)
        logging.info("✍️ Adding caption...")
        pg.write(message, interval=0.02)
        time.sleep(1)
        
        # Step 6: Send the image with caption
        logging.info("📤 Sending message with image...")
        pg.press('enter')
        time.sleep(3)
        
        # Close tab
        logging.info("🔒 Closing tab...")
        pg.hotkey('ctrl', 'w')
        
        logging.info("✅ Message with image sent successfully!")
        return True
        
    except Exception as e:
        logging.error(f"❌ Error in send_whatsapp_with_image_v2: {e}")
        return False


def _copy_image_to_clipboard(image_path):
    """
    Copy image to clipboard using Linux tools (wl-copy for Wayland, xclip for X11)
    """
    import subprocess
    
    # Determine image type
    mime_type = "image/jpeg"
    if image_path.lower().endswith('.png'):
        mime_type = "image/png"
    elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
        mime_type = "image/jpeg"
    
    try:
        # Try Wayland (wl-copy) first
        cmd = f"wl-copy < '{image_path}' --type {mime_type}"
        result = subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
        if result.returncode == 0:
            logging.info(f"✅ Image copied to clipboard (Wayland) - {mime_type}")
            return True
        else:
            # Try alternative wl-copy syntax
            cmd = f"cat '{image_path}' | wl-copy --type {mime_type}"
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            if result.returncode == 0:
                logging.info(f"✅ Image copied to clipboard (Wayland/cat) - {mime_type}")
                return True
    except Exception as e:
        logging.debug(f"Wayland clipboard failed: {e}")
        pass
    
    try:
        # Fallback to X11 (xclip)
        cmd = f"xclip -selection clipboard -t {mime_type} -i '{image_path}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
        if result.returncode == 0:
            logging.info(f"✅ Image copied to clipboard (X11) - {mime_type}")
            return True
    except Exception as e:
        logging.debug(f"X11 clipboard failed: {e}")
        pass
    
    logging.error("❌ Failed to copy image to clipboard (tried wl-copy and xclip)")
    return False


# Main function to use (automatically picks best method)
def send_alert_with_image(phone_no, animal_name, image_path):
    """
    Main wrapper function that sends WhatsApp alert with image.
    Uses the most reliable v3 method with better debugging.
    
    Args:
        phone_no (str): Phone number with country code (e.g., "+918100661171")
        animal_name (str): Name of detected animal
        image_path (str): Path to captured image
    
    Returns:
        bool: True if sent successfully
    """
    message = f"🚨 THREAT DETECTED: {animal_name} has breached the perimeter!"
    
    logging.info(f"=" * 60)
    logging.info(f"STARTING WHATSAPP SEND")
    logging.info(f"Phone: {phone_no}")
    logging.info(f"Animal: {animal_name}")
    logging.info(f"Image: {image_path}")
    logging.info(f"Image exists: {os.path.exists(image_path)}")
    logging.info(f"=" * 60)
    
    # Try v3 method first (most reliable)
    logging.info("Attempting V3 method (direct browser + clipboard)...")
    success = send_whatsapp_with_image_v3(phone_no, message, image_path)
    
    if not success:
        logging.warning("⚠️ V3 failed, trying V2 (pywhatkit + clipboard)...")
        success = send_whatsapp_with_image_v2(phone_no, message, image_path)
    
    if not success:
        logging.warning("⚠️ V2 failed, trying V1 (fallback method)...")
        success = send_whatsapp_with_image(phone_no, message, image_path)
    
    if success:
        logging.info("✅✅✅ IMAGE SENT SUCCESSFULLY ✅✅✅")
    else:
        logging.error("❌❌❌ ALL METHODS FAILED ❌❌❌")
    
    return success

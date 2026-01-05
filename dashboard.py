import streamlit as st
import cv2
import time
import os
import threading
import subprocess
from datetime import datetime
from ultralytics import YOLO
import pygame  # NOW INSTALLED
# Import the improved WhatsApp sender
from ai_core.whatsapp_sender import send_alert_with_image

# --- CONFIGURATION ---
st.set_page_config(page_title="DrishtiX Command Center", layout="wide", page_icon="🐘")
TARGET_PHONE = "+918100661171"  # Your verified number
SIREN_FILE = "alarm.mp3"        # Must be in the same folder

# --- INITIALIZE AUDIO ---
try:
    pygame.mixer.init()
    # Check if file exists to prevent crash
    if not os.path.exists(SIREN_FILE):
        st.error(f"⚠️ MISSING SOUND FILE: {SIREN_FILE}. Please download it!")
except Exception as e:
    print(f"Audio Init Error: {e}")

# Custom CSS
st.markdown("""
<style>
    .reportview-container { background: #0e1117; }
    .main-header { font-size: 2.5rem; color: #FF4B4B; text-align: center; font-weight: bold; }
    .metric-box { background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #444; text-align: center; }
    .alert-log { background-color: #330000; color: #ffcccc; padding: 10px; border-radius: 5px; margin-bottom: 5px; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL STATE ---
if 'alert_history' not in st.session_state:
    st.session_state['alert_history'] = []
if 'last_alert_time' not in st.session_state:
    st.session_state['last_alert_time'] = 0

# --- HELPER FUNCTIONS ---
def get_next_image_path(animal_name):
    """Creates breached folder and returns sequential image path"""
    # Create breached folder if it doesn't exist
    breached_folder = "breached"
    os.makedirs(breached_folder, exist_ok=True)
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Count existing files to get sequence number
    existing_files = [f for f in os.listdir(breached_folder) if f.endswith('.jpg')]
    sequence = len(existing_files) + 1
    
    # Create filename: breached/0001_ELEPHANT_20260105_143022.jpg
    filename = f"{sequence:04d}_{animal_name.replace(' ', '_')}_{timestamp}.jpg"
    filepath = os.path.join(breached_folder, filename)
    
    return os.path.abspath(filepath)

def play_siren():
    """Plays the alarm sound safely"""
    try:
        if os.path.exists(SIREN_FILE):
            # Stop previous sound if playing
            if pygame.mixer.music.get_busy():
                return
            pygame.mixer.music.load(SIREN_FILE)
            pygame.mixer.music.play()
    except Exception as e:
        print(f"Siren failed: {e}")

def send_whatsapp_thread(image_path, animal_name, phone_no):
    """Runs in background to avoid freezing the video feed"""
    try:
        print(f"🚀 Sending WhatsApp Alert for {animal_name}...")
        
        # Use the improved image sending function
        success = send_alert_with_image(phone_no, animal_name, image_path)
        
        if success:
            print("✅ Alert with image sent successfully!")
        else:
            print("❌ Failed to send alert with image")

    except Exception as e:
        print(f"❌ Failed to send WhatsApp: {e}")

# --- SIDEBAR ---
st.sidebar.image("https://img.icons8.com/color/96/000000/elephant.png", width=100)
st.sidebar.title("🔧 System Config")
conf_threshold = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.4, 0.05)
enable_notifications = st.sidebar.checkbox("Enable Alerts (Siren + WA)", value=True)
model_path = st.sidebar.text_input("Model Path", "ai_core/models/best.pt")

# --- MAIN LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="main-header">🐘 DrishtiX Surveillance Feed</div>', unsafe_allow_html=True)
    video_placeholder = st.empty()
    stop_button = st.button("⏹ Stop System")

with col2:
    st.markdown("### 📊 Live Telemetry")
    m1, m2 = st.columns(2)
    with m1: status_text = st.empty()
    with m2: object_text = st.empty()

    st.markdown("---")
    st.markdown("### 🚨 Alert Log")
    log_placeholder = st.empty()

# --- LOAD MODEL ---
@st.cache_resource
def load_model(path):
    return YOLO(path)

try:
    model = load_model(model_path)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- VIDEO LOOP ---
cap = cv2.VideoCapture(0)
target_animals = ["Elephant", "elephant", "elephants", "Wild Boar", "wild boar"]
ALERT_COOLDOWN = 60

while cap.isOpened() and not stop_button:
    ret, frame = cap.read()
    if not ret:
        st.error("Camera not found!")
        break

    # AI Detection
    results = model(frame, stream=True, verbose=False)
    threat_detected = False
    detected_name = "None"

    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            name = model.names[cls]

            if conf > conf_threshold:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                color = (0, 255, 0)

                if name in target_animals:
                    threat_detected = True
                    detected_name = name
                    color = (0, 0, 255)

                    # Draw Box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
                    cv2.putText(frame, f"THREAT: {name.upper()}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

                    # --- ALERT SYSTEM ---
                    current_time = time.time()
                    if enable_notifications and (current_time - st.session_state['last_alert_time'] > ALERT_COOLDOWN):
                        st.session_state['last_alert_time'] = current_time

                        # 1. PLAY SOUND
                        play_siren()

                        # 2. SHOW VISUAL
                        st.toast(f"🚨 ALERT TRIGGERED: {detected_name}!", icon="🔊")

                        # 3. SAVE EVIDENCE WITH SEQUENTIAL NAMING
                        evidence_path = get_next_image_path(detected_name)
                        cv2.imwrite(evidence_path, frame)
                        print(f"📸 Evidence saved: {evidence_path}")
                        
                        # 4. SEND WHATSAPP
                        t = threading.Thread(target=send_whatsapp_thread, args=(evidence_path, detected_name, TARGET_PHONE))
                        t.start()
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{name} {conf:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # UI Refresh
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

    if threat_detected:
        status_text.markdown('<div class="metric-box" style="background:#800000; color:white;">🔥 STATUS: CRITICAL</div>', unsafe_allow_html=True)
        object_text.metric("Detected Threat", detected_name)

        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] ⚠️ {detected_name} Detected!"
        if not st.session_state['alert_history'] or st.session_state['alert_history'][-1] != log_entry:
             st.session_state['alert_history'].append(log_entry)
    else:
        status_text.markdown('<div class="metric-box" style="background:#004d00; color:white;">✅ STATUS: SECURE</div>', unsafe_allow_html=True)
        object_text.metric("Detected Threat", "None")

    # Render Log
    log_html = ""
    for log in reversed(st.session_state['alert_history'][-8:]):
        log_html += f'<div class="alert-log">{log}</div>'
    log_placeholder.markdown(log_html, unsafe_allow_html=True)

cap.release()

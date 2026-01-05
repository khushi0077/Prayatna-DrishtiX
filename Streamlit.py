import streamlit as st
import cv2
import serial
import time
import requests
import threading
from ultralytics import YOLO

BLYNK_AUTH = "XVhF_-ZPxwBHl8wpmnAS39h2XzW6oEsr"
BLYNK_URL = "blynk.cloud"
COM_PORT = "COM17" 

if 'ser' not in st.session_state:
    try:
        st.session_state.ser = serial.Serial(COM_PORT, 9600, timeout=1)
        time.sleep(2)
    except:
        st.session_state.ser = None

def trigger_cloud_alert(is_active):
    value = 1 if is_active else 0
    link = f"https://{BLYNK_URL}/external/api/update?token={BLYNK_AUTH}&V1={value}"
    try:
        requests.get(link)
    except:
        pass

def trigger_hardware(command):
    if st.session_state.ser:
        try:
            st.session_state.ser.write(command.encode())
        except:
            pass

st.title("DrishtiX Protection System")
left_col, right_col = st.columns([2, 1])

with right_col:
    st.subheader("Live Data")
    distance_text = st.empty()
    alert_status = st.empty()
    wake_threshold = st.slider("Wake Up Distance (cm)", 10, 300, 100)

with left_col:
    system_on = st.checkbox("Activate System", value=True)
    camera_feed = st.image([])
    
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)
    
    is_alerting = False

    while system_on and cap.isOpened():
        current_distance = 999
        if st.session_state.ser and st.session_state.ser.in_waiting:
            try:
                raw_data = st.session_state.ser.readline().decode().strip()
                if raw_data.startswith("D:"):
                    current_distance = int(raw_data.split(":")[1])
                    distance_text.metric("Sensor", f"{current_distance} cm")
            except:
                pass
        
        animal_detected = False
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if current_distance < wake_threshold:
            results = model(frame, verbose=False)
            frame = results[0].plot()
            
            for box in results[0].boxes:
                class_id = int(box.cls[0])
                if class_id in [20, 16, 21]: 
                    animal_detected = True
                    break
        
        if animal_detected:
            if not is_alerting:
                trigger_hardware('1')
                threading.Thread(target=trigger_cloud_alert, args=(True,)).start()
                is_alerting = True
                alert_status.error("Danger Detected")
        else:
            if is_alerting:
                trigger_hardware('0')
                threading.Thread(target=trigger_cloud_alert, args=(False,)).start()
                is_alerting = False
                alert_status.success("Area Safe")

        camera_feed.image(frame, channels='BGR')

    cap.release()
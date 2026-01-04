import cv2
import serial
import time
import os
import sys
from ultralytics import YOLO

# --- 1. SETUP PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")

# --- 2. CONFIGURATION ---
# LOWERED THIS to 0.20 to catch everything!
CONF_THRESHOLD = 0.20 

# --- 3. INITIALIZE ---
print(f"Loading Model: {MODEL_PATH}")
try:
    model = YOLO(MODEL_PATH)
    print(f"✅ Model Loaded Successfully!")
    print(f"🧠 KNOWLEDGE CHECK: This model knows these classes: {model.names}")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Helper Scripts (Optional)
try:
    from aggression_tracker import AggressionTracker
    tracker = AggressionTracker()
except:
    tracker = None

# Serial (Optional)
try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    print("✅ ESP32 Connected")
except:
    print("⚠️ No ESP32 found (Simulation Mode)")
    ser = None

# --- 4. MAIN LOOP ---
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

print(">>> CAMERA ACTIVE. SHOW AN IMAGE NOW! <<<")

while True:
    success, img = cap.read()
    if not success: break

    # Run AI
    results = model(img, stream=True, verbose=False)
    
    threat_detected = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Get Data
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            name = model.names[cls]

            # --- DEBUG PRINT (Look at your terminal!) ---
            # This tells us exactly what the AI sees
            print(f"👀 I see a '{name}' with {conf:.2f} confidence.")

            if conf > CONF_THRESHOLD:
                # Draw Box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f"{name} {conf:.2f}", (x1, y1-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Check for Specific Animals (Case-Insensitive)
                # We convert to .lower() to fix "Elephant" vs "elephant" issues
                # We check for both singular ("elephant") and plural ("elephants")
                # Giraffes are NOT in this list, so they are automatically ignored.
                target_animals = ["elephant", "elephants", "wild boar", "wild boars", "boar", "tiger"]
                
                if name.lower() in target_animals:
                    threat_detected = True
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(img, "THREAT DETECTED", (x1, y1-30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Hardware Trigger
    if ser:
        ser.write(b'1' if threat_detected else b'0')

    cv2.imshow('DrishtiX DEBUG MODE', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if ser: ser.close()

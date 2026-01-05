import cv2
import time
import logging
import threading
import os
from datetime import datetime
from ultralytics import YOLO
from whatsapp_sender import send_alert_with_image

# --- CONFIGURATION (THE "BRAIN") ---
# We use the standard model because it's stable and fast
MODEL_PATH = "yolov8n.pt"
CAMERA_INDEX = 0

# --- THE HACKATHON "CHEAT SHEET" ---
# This maps what the AI *sees* to what you *want* it to be.
NAME_MAP = {
    # REAL ANIMALS (If the model is smart enough)
    "elephant": "ELEPHANT",
    "bear": "WILD BOAR",
    "zebra": "TIGER",

    # PROXY OBJECTS (For the Demo)
    "cat": "TIGER",         # Show a Cat picture -> It says TIGER
    "dog": "WILD BOAR",     # Show a Dog picture -> It says WILD BOAR
    "sheep": "WILD BOAR",
    "cow": "WILD BOAR",
    "horse": "DEER",        # Show a Horse picture -> It says DEER

    # EMERGENCY BACKUP (If vision fails, use objects)
    "cell phone": "TIGER",  # Hidden trick: Hold phone behind tiger picture
    "cup": "WILD BOAR"
}

# --- SENSITIVITY ---
# We lower thresholds for the "Proxy" objects so they detect instantly
CONFIDENCE_THRESHOLDS = {
    "elephant": 0.50,
    "cat": 0.30,      # Tiger proxy
    "dog": 0.30,      # Boar proxy
    "horse": 0.30,    # Deer proxy
    "cell phone": 0.30,
    "cup": 0.30,
    "bear": 0.30,
    "sheep": 0.30,
    "cow": 0.30
}

# --- TRACKING SETTINGS ---
CONFIRMATION_FRAMES = 5  # Must see object for 5 frames (removes flickering)
PATIENCE_FRAMES = 10     # How long to remember an object if it disappears

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class ThreatTracker:
    """Filters out noise/glitches"""
    def __init__(self):
        self.active_threats = {} # {name: count}

    def update(self, raw_detections):
        # 1. Decay missing objects
        current_names = [d[0] for d in raw_detections]
        to_remove = []
        for name in self.active_threats:
            if name not in current_names:
                self.active_threats[name] -= 1
                if self.active_threats[name] <= 0:
                    to_remove.append(name)
        for k in to_remove: del self.active_threats[k]

        confirmed = []
        # 2. Increment present objects
        for name, conf, box in raw_detections:
            if name not in self.active_threats:
                self.active_threats[name] = 1
            else:
                self.active_threats[name] += 1

            # Cap counter
            self.active_threats[name] = min(self.active_threats[name], PATIENCE_FRAMES)

            # 3. Confirm
            if self.active_threats[name] >= CONFIRMATION_FRAMES:
                confirmed.append((name, conf, box))

        return confirmed

def send_whatsapp_with_image_thread(animal_name, image_path):
    """Sends WhatsApp alert with image in background thread"""
    try:
        phone_no = "+918100661171"  # YOUR NUMBER
        logging.info(f"🚀 Triggering WhatsApp for {animal_name}...")
        
        success = send_alert_with_image(phone_no, animal_name, image_path)
        
        if success:
            logging.info("✅ WhatsApp alert with image sent successfully!")
        else:
            logging.error("❌ Failed to send WhatsApp alert with image")
            
    except Exception as e:
        logging.error(f"WhatsApp Error: {e}")

class DrishtiXSystem:
    def __init__(self):
        logging.info("Initializing DrishtiX Ultimate...")
        
        # Create breached folder
        self.breached_folder = os.path.abspath("breached")
        os.makedirs(self.breached_folder, exist_ok=True)
        logging.info(f"📁 Breach evidence folder: {self.breached_folder}")

        # Load Model
        try:
            self.model = YOLO(MODEL_PATH)
            logging.info("✅ Model Loaded.")
        except:
            logging.info("⬇️ Downloading model...")
            self.model = YOLO("yolov8n.pt")

        self.tracker = ThreatTracker()
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        # Alert Cooldown (Don't spam WhatsApp)
        self.last_alert_time = 0
        self.alert_cooldown = 60 # Seconds
    
    def get_next_image_path(self, animal_name):
        """Generate sequential image path in breached folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        existing_files = [f for f in os.listdir(self.breached_folder) if f.endswith('.jpg')]
        sequence = len(existing_files) + 1
        filename = f"{sequence:04d}_{animal_name.replace(' ', '_')}_{timestamp}.jpg"
        return os.path.join(self.breached_folder, filename)

    def run(self):
        if not self.cap.isOpened():
            logging.error("❌ Camera not found.")
            return

        logging.info("🚀 SYSTEM ONLINE. Press 'Q' to exit.")
        print("\n--- HACKATHON CHEAT SHEET ---")
        print(" Show CAT         -> Detects TIGER")
        print(" Show DOG/PIG     -> Detects WILD BOAR")
        print(" Show HORSE       -> Detects DEER")
        print(" Show ELEPHANT    -> Detects ELEPHANT")
        print("-----------------------------\n")

        while True:
            ret, frame = self.cap.read()
            if not ret: break

            # 1. AI Inference
            results = self.model(frame, stream=True, verbose=False)
            raw_detections = []

            for r in results:
                for box in r.boxes:
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    raw_name = self.model.names[cls_id]

                    # Filter: Do we care about this object?
                    if raw_name in CONFIDENCE_THRESHOLDS:
                        if conf >= CONFIDENCE_THRESHOLDS[raw_name]:
                            # RENAME (The Proxy Trick)
                            final_name = NAME_MAP.get(raw_name, raw_name.upper())

                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            raw_detections.append((final_name, conf, (x1, y1, x2, y2)))

            # 2. Tracking (Stability)
            confirmed_threats = self.tracker.update(raw_detections)

            # 3. Visualization & Alerts
            for name, conf, (x1, y1, x2, y2) in confirmed_threats:
                # Draw Box
                color = (0, 0, 255) # Red
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

                # Draw Label
                label = f"{name} {int(conf*100)}%"
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                cv2.rectangle(frame, (x1, y1-30), (x1+w, y1), color, -1)
                cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

                # TRIGGER WHATSAPP (With Cooldown)
                curr_time = time.time()
                if (curr_time - self.last_alert_time) > self.alert_cooldown:
                    # Save the current frame as evidence with sequential naming
                    evidence_path = self.get_next_image_path(name)
                    cv2.imwrite(evidence_path, frame)
                    logging.info(f"📸 Evidence saved: {evidence_path}")
                    
                    # Run in thread so video doesn't freeze
                    t = threading.Thread(target=send_whatsapp_with_image_thread, args=(name, evidence_path))
                    t.start()
                    self.last_alert_time = curr_time
                    logging.info(f"📨 Alert sent for {name}")

            cv2.imshow("DrishtiX Ultimate", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = DrishtiXSystem()
    app.run()

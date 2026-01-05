#define LED_PIN 2

char command;
unsigned long lastBlink = 0;
unsigned long blinkInterval = 0;
bool ledState = LOW;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    command = Serial.read();
  }

  // RANDOM BLINK PATTERN (Threat Mode)
  if (command == '3') {
    unsigned long now = millis();
    if (now - lastBlink > blinkInterval) {
      ledState = !ledState;
      digitalWrite(LED_PIN, ledState);

      // Random delay between 80ms – 600ms
      blinkInterval = random(80, 600);
      lastBlink = now;
    }
  }

  // SAFE MODE (LED OFF)
  else if (command == '0') {
    digitalWrite(LED_PIN, LOW);
  }
}

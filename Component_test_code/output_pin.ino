/*
=========================================================
12_OUTPUT_PIN_TEST

Hardware
---------
Arduino Uno

Pins Tested
-----------
D4  - Buzzer
D6  - Left VL53L0X XSHUT
D7  - Right VL53L0X XSHUT
D9  - Servo Signal
D11 - Motor PWM
D13 - Motor Direction

Purpose
-------
- Verify every output pin works
- Toggle each pin HIGH then LOW
- Print current pin being tested

Baud Rate
---------
115200
=========================================================
*/

const int pins[] = {4, 6, 7, 9, 11, 13};
const int numPins = sizeof(pins) / sizeof(pins[0]);

void setup() {

  Serial.begin(115200);

  Serial.println();
  Serial.println("==================================");
  Serial.println("OUTPUT PIN TEST");
  Serial.println("==================================");

  for (int i = 0; i < numPins; i++) {
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], LOW);
  }

  Serial.println("Beginning test...");
}

void loop() {

  for (int i = 0; i < numPins; i++) {

    int pin = pins[i];

    Serial.print("Testing D");
    Serial.println(pin);

    // HIGH
    digitalWrite(pin, HIGH);
    Serial.println("  HIGH");
    delay(1000);

    // LOW
    digitalWrite(pin, LOW);
    Serial.println("  LOW");
    delay(1000);

    Serial.println();
  }

  Serial.println("Cycle complete.");
  Serial.println("-------------------------");
  delay(2000);
}

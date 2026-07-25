#include <Servo.h>

Servo servo;

void setup() {
  Serial.begin(9600);
  servo.attach(9);
  servo.write(90);
}

void loop() {

  if (Serial.available()) {

    char cmd = Serial.read();

    if (cmd == 'R') {
      servo.write(60);
    }

    else if (cmd == 'L') {
      servo.write(120);
    }

    else if (cmd == 'C') {
      servo.write(90);
    }

    // Flush the newline character
    while (Serial.available()) {
      Serial.read();
    }
  }
}

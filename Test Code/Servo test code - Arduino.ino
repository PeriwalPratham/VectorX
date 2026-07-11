#include <Servo.h>
Servo servo;
int currentAngle = 90;

void setup() {
  Serial.begin(9600);
  servo.attach(9);
  servo.write(90);
  Serial.println("Arduino connected!");
  Serial.println("Use this port for Python:");
}

void loop() {
  if (Serial.available()) {
    int targetAngle = Serial.parseInt();
    targetAngle = constrain(
      targetAngle,
      0,
      180
    );
    if (currentAngle < targetAngle) {
      currentAngle++;
    }
    else if (currentAngle > targetAngle) {
      currentAngle--;
    }
    servo.write(currentAngle);
  }
  delay(15);
}

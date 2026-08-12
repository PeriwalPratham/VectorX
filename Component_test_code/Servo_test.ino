#include <Servo.h>

Servo steeringServo;

const int SERVO_PIN = 9;

// Adjust these if needed
const int LEFT = 102;
const int CENTRE = 82;
const int RIGHT = 62;

void setup() {
  Serial.begin(115200);

  steeringServo.attach(SERVO_PIN);

  Serial.println();
  Serial.println("========== SERVO TEST ==========");
  Serial.println("Automatic test starting...");
  Serial.println();
}

void loop() {

  // Automatic movement
  Serial.println("LEFT");
  steeringServo.write(LEFT);
  delay(1000);

  Serial.println("CENTRE");
  steeringServo.write(CENTRE);
  delay(1000);

  Serial.println("RIGHT");
  steeringServo.write(RIGHT);
  delay(1000);

  Serial.println("CENTRE");
  steeringServo.write(CENTRE);
  delay(1000);

  // Manual control
  if (Serial.available()) {

    int angle = Serial.parseInt();

    if (angle >= 0 && angle <= 180) {

      steeringServo.write(angle);

      Serial.print("Moved to ");
      Serial.print(angle);
      Serial.println(" degrees");

    } else {

      Serial.println("Invalid angle (0-180)");

    }

    while (Serial.available())
      Serial.read();
  }
}

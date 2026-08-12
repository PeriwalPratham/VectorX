/*
=========================================================
06_MOTOR_SERVO_TEST

Hardware
---------
Arduino Uno
Arduino L298P Motor Shield
REV Robotics Smart Servo
N20 600 RPM Motor

Pins
----
Servo      -> D9
Motor PWM  -> D11
Motor DIR  -> D13

Purpose
-------
- Verify steering while driving
- Verify motor + servo together
- Manual serial control

Baud Rate
---------
115200

Commands
--------
L = Left
C = Centre
R = Right
F = Forward
B = Reverse
S = Stop
=========================================================
*/

#include <Servo.h>

Servo steeringServo;

const int SERVO_PIN = 9;
const int PWM_PIN   = 11;
const int DIR_PIN   = 13;

const int LEFT   = 102;
const int CENTRE = 82;
const int RIGHT  = 62;

const int SPEED = 150;

void stopMotor() {
  analogWrite(PWM_PIN, 0);
}

void forward() {
  digitalWrite(DIR_PIN, HIGH);
  analogWrite(PWM_PIN, SPEED);
}

void reverse() {
  digitalWrite(DIR_PIN, LOW);
  analogWrite(PWM_PIN, SPEED);
}

void setup() {

  Serial.begin(115200);

  steeringServo.attach(SERVO_PIN);

  pinMode(PWM_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);

  stopMotor();
  steeringServo.write(CENTRE);

  Serial.println();
  Serial.println("====================================");
  Serial.println("Motor + Servo Test");
  Serial.println("====================================");
}

void loop() {

  // -------------------------
  // Automatic Demonstration
  // -------------------------

  Serial.println("Forward + Centre");
  steeringServo.write(CENTRE);
  forward();
  delay(2000);

  Serial.println("Forward + Left");
  steeringServo.write(LEFT);
  delay(2000);

  Serial.println("Forward + Centre");
  steeringServo.write(CENTRE);
  delay(2000);

  Serial.println("Forward + Right");
  steeringServo.write(RIGHT);
  delay(2000);

  Serial.println("Stop");
  stopMotor();
  steeringServo.write(CENTRE);

  Serial.println();
  Serial.println("Manual Mode");
  Serial.println("L C R F B S");

  // -------------------------
  // Manual Control
  // -------------------------

  while (true) {

    if (Serial.available()) {

      char cmd = toupper(Serial.read());

      switch (cmd) {

        case 'L':
          steeringServo.write(LEFT);
          Serial.println("Steering LEFT");
          break;

        case 'C':
          steeringServo.write(CENTRE);
          Serial.println("Steering CENTRE");
          break;

        case 'R':
          steeringServo.write(RIGHT);
          Serial.println("Steering RIGHT");
          break;

        case 'F':
          forward();
          Serial.println("Motor FORWARD");
          break;

        case 'B':
          reverse();
          Serial.println("Motor REVERSE");
          break;

        case 'S':
          stopMotor();
          Serial.println("Motor STOPPED");
          break;
      }
    }
  }
}


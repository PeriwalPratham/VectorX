#include <Wire.h>
#include <VL53L0X.h>
#include <Servo.h>

VL53L0X leftSensor;
VL53L0X rightSensor;
Servo steeringServo;

// Motor Shield Pins
const int pwmPin = 11;
const int dirPin = 13;

// Servo
const int SERVO_PIN = 9;

// ToF XSHUT Pins
const int LEFT_XSHUT = 6;
const int RIGHT_XSHUT = 7;

// Steering Angles
const int STRAIGHT = 90;
const int RIGHT = 65;
const int LEFT = 115;

bool correctingLeft = false;
bool leftSensorOK = false;

void setup() {
  Serial.begin(9600);

  pinMode(pwmPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  steeringServo.attach(SERVO_PIN);
  steeringServo.write(STRAIGHT);

  stopMotor();

  Wire.begin();

  pinMode(LEFT_XSHUT, OUTPUT);
  pinMode(RIGHT_XSHUT, OUTPUT);

  // Turn both sensors off
  digitalWrite(LEFT_XSHUT, LOW);
  digitalWrite(RIGHT_XSHUT, LOW);
  delay(10);

  // Initialize left sensor
  digitalWrite(LEFT_XSHUT, HIGH);
  delay(10);

  leftSensorOK = leftSensor.init();

  if (leftSensorOK) {
    leftSensor.setAddress(0x30);
    leftSensor.setTimeout(100);
    leftSensor.startContinuous();
    Serial.println("Left VL53L0X initialized.");
  } else {
    Serial.println("Left VL53L0X not found. Continuing without it.");
  }

  // Initialize right sensor
  digitalWrite(RIGHT_XSHUT, HIGH);
  delay(10);

  if (!rightSensor.init()) {
    Serial.println("Right VL53L0X not found!");
    while (1);
  }

  rightSensor.setAddress(0x31);
  rightSensor.setTimeout(100);
  rightSensor.startContinuous();

  Serial.println("System Ready");
}

void loop() {

  uint16_t leftDistance = 0;

  if (leftSensorOK) {
    leftDistance = leftSensor.readRangeContinuousMillimeters();
  }

  uint16_t rightDistance = rightSensor.readRangeContinuousMillimeters();

  Serial.print("Left: ");
  if (leftSensorOK)
    Serial.print(leftDistance);
  else
    Serial.print("N/A");

  Serial.print(" mm\t");

  Serial.print("Right: ");
  Serial.print(rightDistance);
  Serial.println(" mm");

  // Use ONLY the right sensor for navigation
  uint16_t distance = rightDistance;

  // Keep the <100 mm left correction logic
  if (distance < 200) {
    correctingLeft = true;
  }
  else if (distance >= 250) {
    correctingLeft = false;
  }

  // Too close → steer left
  if (correctingLeft) {
    steeringServo.write(LEFT);
    moveForward(255);
  }

  // Lost the wall → complete one full turn (800 ms)
  else if (rightSensor.timeoutOccurred() ||
           distance == 8190 ||
           distance == 65535 ||
           distance > 400) {

    steeringServo.write(RIGHT);
    moveForward(255);

    // Ignore the sensor while turning
    delay(800);

    steeringServo.write(STRAIGHT);
    moveForward(255);
  }

  // Normal driving
  else {
    steeringServo.write(STRAIGHT);
    moveForward(255);
  }
}

void moveForward(int speedValue) {
  digitalWrite(dirPin, HIGH);   // Change to LOW if motor runs backward
  analogWrite(pwmPin, speedValue);
}

void moveBackward(int speedValue) {
  digitalWrite(dirPin, LOW);    // Change to HIGH if motor runs backward
  analogWrite(pwmPin, speedValue);
}

void stopMotor() {
  analogWrite(pwmPin, 0);
}

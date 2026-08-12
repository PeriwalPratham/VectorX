#include <Servo.h>

// --- SERVO SETUP ---
Servo steeringServo;
const int SERVO_PIN = 9;

const int STRAIGHT = 85;     // Center angle

// Right Dodge Angles (Red)
const int RIGHT_10 = 75;     // -10 deg
const int RIGHT_17 = 68;     // -17 deg
const int RIGHT_20 = 65;     // -20 deg

// Left Dodge Angles (Green)
const int LEFT_10 = 95;      // +10 deg
const int LEFT_17 = 102;     // +17 deg
const int LEFT_20 = 105;     // +20 deg

// --- L298N MOTOR DRIVER PINS ---
const int ENA_PIN = 11; 
const int IN1_PIN = 12; 
const int IN2_PIN = 13; 
const int DRIVE_SPEED = 180; 

// --- CONTROL FLAGS ---
bool isRunning = false;
String currentCommand = "G";

void setup() {
  Serial.begin(115200);

  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  
  steeringServo.attach(SERVO_PIN);
  steeringServo.write(STRAIGHT);

  stopMotor();
}

void loop() {
  readSerialFromPi();

  if (!isRunning || currentCommand == "S") {
    stopMotor();
    steeringServo.write(STRAIGHT);
    return;
  }

  // --- RED DODGE COMMANDS ---
  if (currentCommand == "R10") {
    steeringServo.write(RIGHT_10);
  } 
  else if (currentCommand == "R17") {
    steeringServo.write(RIGHT_17);
  } 
  else if (currentCommand == "R20") {
    steeringServo.write(RIGHT_20);
  } 

  // --- GREEN DODGE COMMANDS ---
  else if (currentCommand == "L10") {
    steeringServo.write(LEFT_10);
  } 
  else if (currentCommand == "L17") {
    steeringServo.write(LEFT_17);
  } 
  else if (currentCommand == "L20") {
    steeringServo.write(LEFT_20);
  } 

  // --- STRAIGHT COMMAND ---
  else if (currentCommand == "G") {
    steeringServo.write(STRAIGHT);
  }

  moveForward();
}

void readSerialFromPi() {
  static String buffer = "";

  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      buffer.trim();
      if (buffer.length() > 0) {
        currentCommand = buffer;
        if (currentCommand == "S") {
          isRunning = false;
        } else {
          isRunning = true;
        }
      }
      buffer = "";
    } else {
      buffer += c;
    }
  }
}

void moveForward() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENA_PIN, DRIVE_SPEED);
}

void stopMotor() {
  analogWrite(ENA_PIN, 0);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
}

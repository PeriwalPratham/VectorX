/*
=========================================================
13_FULL_HARDWARE_TEST

Hardware
---------
Arduino Uno
Arduino L298P Motor Shield
REV Smart Servo
N20 600 RPM Motor
2x Pololu VL53L0X
MPU6050
Buzzer

Purpose
-------
Runs a complete hardware diagnostic.

=========================================================
*/

#include <Wire.h>
#include <Servo.h>
#include <VL53L0X.h>

Servo steeringServo;

VL53L0X leftSensor;
VL53L0X rightSensor;

const int SERVO_PIN = 9;

const int PWM_PIN = 11;
const int DIR_PIN = 13;

const int BUZZER_PIN = 4;

const int LEFT_XSHUT = 6;
const int RIGHT_XSHUT = 7;

const int MPU = 0x68;

void printResult(String name, bool ok)
{
  Serial.print(name);

  for(int i=name.length(); i<18; i++)
    Serial.print(".");

  if(ok)
    Serial.println("PASS");
  else
    Serial.println("FAIL");
}

void setup()
{
  Serial.begin(115200);
  Wire.begin();

  Serial.println();
  Serial.println("====================================");
  Serial.println("FULL HARDWARE DIAGNOSTIC");
  Serial.println("====================================");
  Serial.println();

  bool servoOK = true;
  bool motorOK = true;
  bool buzzerOK = true;
  bool leftOK = true;
  bool rightOK = true;
  bool imuOK = true;

  // -------------------------
  // Servo
  // -------------------------

  steeringServo.attach(SERVO_PIN);

  steeringServo.write(89);
  delay(500);

  steeringServo.write(119);
  delay(500);

  steeringServo.write(69);
  delay(500);

  steeringServo.write(89);

  Serial.println("Observe servo movement.");

  // -------------------------
  // Motor
  // -------------------------

  pinMode(PWM_PIN,OUTPUT);
  pinMode(DIR_PIN,OUTPUT);

  digitalWrite(DIR_PIN,HIGH);
  analogWrite(PWM_PIN,150);
  delay(1000);

  analogWrite(PWM_PIN,0);
  delay(500);

  digitalWrite(DIR_PIN,LOW);
  analogWrite(PWM_PIN,150);
  delay(1000);

  analogWrite(PWM_PIN,0);

  Serial.println("Observe motor movement.");

  // -------------------------
  // Buzzer
  // -------------------------

  pinMode(BUZZER_PIN,OUTPUT);

  tone(BUZZER_PIN,1500,300);
  delay(500);

  Serial.println("Listen for buzzer.");

  // -------------------------
  // Dual ToF
  // -------------------------

  pinMode(LEFT_XSHUT,OUTPUT);
  pinMode(RIGHT_XSHUT,OUTPUT);

  digitalWrite(LEFT_XSHUT,LOW);
  digitalWrite(RIGHT_XSHUT,LOW);

  delay(20);

  digitalWrite(LEFT_XSHUT,HIGH);
  delay(20);

  if(!leftSensor.init())
    leftOK=false;
  else
    leftSensor.setAddress(0x30);

  digitalWrite(RIGHT_XSHUT,HIGH);
  delay(20);

  if(!rightSensor.init())
    rightOK=false;
  else
    rightSensor.setAddress(0x31);

  if(leftOK)
    leftSensor.startContinuous();

  if(rightOK)
    rightSensor.startContinuous();

  // -------------------------
  // MPU6050
  // -------------------------

  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0);

  if(Wire.endTransmission()!=0)
    imuOK=false;

  // -------------------------
  // Report
  // -------------------------

  Serial.println();
  Serial.println("==============================");
  Serial.println("RESULTS");
  Serial.println("==============================");

  printResult("Servo",servoOK);
  printResult("Motor",motorOK);
  printResult("Buzzer",buzzerOK);
  printResult("Left ToF",leftOK);
  printResult("Right ToF",rightOK);
  printResult("MPU6050",imuOK);

  Serial.println();

  if(leftOK)
  {
    Serial.print("Left Distance : ");
    Serial.print(leftSensor.readRangeContinuousMillimeters());
    Serial.println(" mm");
  }

  if(rightOK)
  {
    Serial.print("Right Distance: ");
    Serial.print(rightSensor.readRangeContinuousMillimeters());
    Serial.println(" mm");
  }

  Serial.println();
  Serial.println("Diagnostics complete.");
}

void loop()
{
}

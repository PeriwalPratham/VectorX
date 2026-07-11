#include <Wire.h>
#include <Adafruit_VL53L0X.h>

#define LEFT_XSHUT 9
#define RIGHT_XSHUT 8

Adafruit_VL53L0X leftSensor;
Adafruit_VL53L0X rightSensor;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Serial.println("Starting");
  pinMode(LEFT_XSHUT, OUTPUT);
  pinMode(RIGHT_XSHUT, OUTPUT);
  digitalWrite(LEFT_XSHUT, LOW);
  digitalWrite(RIGHT_XSHUT, LOW);
  delay(100);
  Serial.println("Turning LEFT on");
  digitalWrite(LEFT_XSHUT, HIGH);
  delay(100);
  if (!leftSensor.begin()) {
    Serial.println("LEFT failed");
    while(1);
   }
   Serial.println("LEFT OK");
   leftSensor.setAddress(0x30);
   Serial.println("Turning RIGHT on");
   digitalWrite(RIGHT_XSHUT, HIGH);
   delay(100);
   if (!rightSensor.begin()) {
     Serial.println("RIGHT failed");
     while(1);
   }
   Serial.println("RIGHT OK");
   rightSensor.setAddress(0x31);
   Serial.println("DONE");
 }

 void loop() {
   VL53L0X_RangingMeasurementData_t left;
   VL53L0X_RangingMeasurementData_t right;
   leftSensor.rangingTest(&left, false);
   rightSensor.rangingTest(&right, false);
   Serial.print("LEFT: ");
   Serial.print(left.RangeMilliMeter);
   Serial.print(" mm   RIGHT: ");
   Serial.print(right.RangeMilliMeter);
   Serial.println(" mm");
   delay(500);
 }

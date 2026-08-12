#include <Wire.h>
#include <VL53L0X.h>

VL53L0X leftSensor;
VL53L0X rightSensor;

const int LEFT_XSHUT = 10;
const int RIGHT_XSHUT = 7;

void setup() {

  Serial.begin(115200);
  Wire.begin();

  pinMode(LEFT_XSHUT, OUTPUT);
  pinMode(RIGHT_XSHUT, OUTPUT);

  // Disable both sensors
  digitalWrite(LEFT_XSHUT, LOW);
  digitalWrite(RIGHT_XSHUT, LOW);
  delay(20);

  // ----------------------------
  // Initialize LEFT sensor
  // ----------------------------
  digitalWrite(LEFT_XSHUT, HIGH);
  delay(20);

  if (!leftSensor.init()) {
    Serial.println("ERROR: Left sensor not found!");
    while (1);
  }

  leftSensor.setAddress(0x30);

  // ----------------------------
  // Initialize RIGHT sensor
  // ----------------------------
  digitalWrite(RIGHT_XSHUT, HIGH);
  delay(20);

  if (!rightSensor.init()) {
    Serial.println("ERROR: Right sensor not found!");
    while (1);
  }

  rightSensor.setAddress(0x31);

  leftSensor.startContinuous();
  rightSensor.startContinuous();

  Serial.println();
  Serial.println("=================================");
  Serial.println("Dual VL53L0X Test Started");
  Serial.println("=================================");
}

void loop() {

  int leftDistance = leftSensor.readRangeContinuousMillimeters();
  int rightDistance = rightSensor.readRangeContinuousMillimeters();

  Serial.print("Left : ");
  Serial.print(leftDistance);
  Serial.print(" mm");

  if (leftSensor.timeoutOccurred())
    Serial.print("  (TIMEOUT)");

  Serial.print("    |    ");

  Serial.print("Right : ");
  Serial.print(rightDistance);
  Serial.print(" mm");

  if (rightSensor.timeoutOccurred())
    Serial.print("  (TIMEOUT)");

  Serial.println();

  delay(100);
}

#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;

void setup() {

  Serial.begin(115200);
  Wire.begin();

  Serial.println();
  Serial.println("=================================");
  Serial.println("Single VL53L0X Test");
  Serial.println("=================================");

  if (!sensor.init()) {
    Serial.println("ERROR: Sensor not detected!");
    while (1);
  }

  sensor.setTimeout(100);
  sensor.startContinuous();

  Serial.println("Sensor initialized successfully.");
}

void loop() {

  uint16_t distance = sensor.readRangeContinuousMillimeters();

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.print(" mm");

  if (sensor.timeoutOccurred()) {
    Serial.print("  (TIMEOUT)");
  }

  Serial.println();

  delay(100);
}


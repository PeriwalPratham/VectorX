#include <Wire.h>
#include <VL53L0X.h>

#define XSHUT_LEFT  6
#define XSHUT_RIGHT 7

#define ADDRESS_LEFT  0x30
#define ADDRESS_RIGHT 0x31

VL53L0X sensorLeft;
VL53L0X sensorRight;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  pinMode(XSHUT_LEFT, OUTPUT);
  pinMode(XSHUT_RIGHT, OUTPUT);

  // Shut down both ToF sensors
  digitalWrite(XSHUT_LEFT, LOW);
  digitalWrite(XSHUT_RIGHT, LOW);
  delay(10);

  // Bring up LEFT ToF, reassign address
  digitalWrite(XSHUT_LEFT, HIGH);
  delay(10);
  sensorLeft.setTimeout(500);
  if (!sensorLeft.init()) {
    Serial.println("Failed to detect LEFT ToF sensor!");
  } else {
    sensorLeft.setAddress(ADDRESS_LEFT);
    Serial.println("Left ToF set to 0x30");
  }

  // Bring up RIGHT ToF, reassign address
  digitalWrite(XSHUT_RIGHT, HIGH);
  delay(10);
  sensorRight.setTimeout(500);
  if (!sensorRight.init()) {
    Serial.println("Failed to detect RIGHT ToF sensor!");
  } else {
    sensorRight.setAddress(ADDRESS_RIGHT);
    Serial.println("Right ToF set to 0x31");
  }

  Serial.println("\nScanning full I2C bus for all devices...\n");
  scanI2C();
}

void loop() {
  // nothing — scan runs once in setup
}

void scanI2C() {
  byte error, address;
  int nDevices = 0;

  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("Device found at 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      nDevices++;
    }
  }

  if (nDevices == 0) {
    Serial.println("No I2C devices found");
  } else {
    Serial.print(nDevices);
    Serial.println(" device(s) found total");
  }
}
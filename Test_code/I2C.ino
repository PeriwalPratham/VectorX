#include <Wire.h>
#include <VL53L0X.h>

#define LEFT_XSHUT   6
#define RIGHT_XSHUT  7

#define LEFT_ADDR    0x30
#define RIGHT_ADDR   0x31
#define MPU_ADDR     0x68

VL53L0X leftSensor;
VL53L0X rightSensor;

bool checkDevice(byte address)
{
  Wire.beginTransmission(address);
  return (Wire.endTransmission() == 0);
}

void setup()
{
  Serial.begin(115200);
  Wire.begin();

  Serial.println();
  Serial.println("==================================");
  Serial.println("VECTORX WRO I2C SCANNER");
  Serial.println("==================================");

  pinMode(LEFT_XSHUT, OUTPUT);
  pinMode(RIGHT_XSHUT, OUTPUT);

  // Turn both sensors off
  digitalWrite(LEFT_XSHUT, LOW);
  digitalWrite(RIGHT_XSHUT, LOW);
  delay(50);

  // -----------------------
  // LEFT SENSOR
  // -----------------------

  digitalWrite(LEFT_XSHUT, HIGH);
  delay(50);

  if (!leftSensor.init())
  {
    Serial.println("Left ToF : FAIL");
  }
  else
  {
    leftSensor.setAddress(LEFT_ADDR);
    Serial.println("Left ToF : PASS");
  }

  // -----------------------
  // RIGHT SENSOR
  // -----------------------

  digitalWrite(RIGHT_XSHUT, HIGH);
  delay(50);

  if (!rightSensor.init())
  {
    Serial.println("Right ToF: FAIL");
  }
  else
  {
    rightSensor.setAddress(RIGHT_ADDR);
    Serial.println("Right ToF: PASS");
  }

  Serial.println();
  Serial.println("Scanning I2C Bus...");
  Serial.println();

  if (checkDevice(LEFT_ADDR))
    Serial.println("Found Left ToF   (0x30)");
  else
    Serial.println("Missing Left ToF (0x30)");

  if (checkDevice(RIGHT_ADDR))
    Serial.println("Found Right ToF  (0x31)");
  else
    Serial.println("Missing Right ToF (0x31)");

  if (checkDevice(MPU_ADDR))
    Serial.println("Found MPU6050    (0x68)");
  else
    Serial.println("Missing MPU6050  (0x68)");

  Serial.println();
  Serial.println("==================================");

  bool allOK =
      checkDevice(LEFT_ADDR) &&
      checkDevice(RIGHT_ADDR) &&
      checkDevice(MPU_ADDR);

  if (allOK)
  {
    Serial.println("ALL I2C DEVICES DETECTED");

    tone(4, 2000, 150);
    delay(200);
    tone(4, 2000, 150);
  }
  else
  {
    Serial.println("CHECK WIRING");

    for (int i = 0; i < 3; i++)
    {
      tone(4, 800, 300);
      delay(400);
    }
  }
}

void loop()
{
}

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

float gyroZOffset = 0;
float heading = 0;

unsigned long lastTime;
bool stopped = false;

void setup() {
  Serial.begin(115200);

  if (!mpu.begin()) {
    Serial.println("MPU6050 not found! Halting.");
    while (1) delay(10);
  }

  mpu.setGyroRange(MPU6050_RANGE_250_DEG); // matches the 131 LSB/(deg/s) sensitivity used below

  Serial.println("Keep the robot still...");
  delay(2000);

  // Calibrate gyro Z offset
  float sum = 0;
  const int samples = 1000;
  for (int i = 0; i < samples; i++) {
    sum += readGyroZ();
    delay(2);
  }
  gyroZOffset = sum / samples;
  Serial.print("Gyro Z Offset: ");
  Serial.println(gyroZOffset);
  Serial.println("Calibration complete!");

  lastTime = micros();
}

void loop() {
  if (stopped) return;

  unsigned long now = micros();
  float dt = (now - lastTime) / 1000000.0;
  lastTime = now;

  float gyroZ = readGyroZ();

  // Already in raw-equivalent units (deg/s * 131), so divide the same way
  float rate = (gyroZ - gyroZOffset) / 131.0;

  // Ignore tiny drift
  if (abs(rate) < 0.5)
    rate = 0;

  // Integrate heading
  heading += rate * dt;

  Serial.print("Heading: ");
  Serial.print(heading, 2);
  Serial.println(" deg");

  if (heading >= 275.0) {
    Serial.println("STOP");
    stopped = true;
  }

  delay(20);
}

// Returns the gyro Z reading scaled to match the old raw register's units
// (LSB counts, i.e. deg/s * 131), so the rest of the logic above doesn't change.
float readGyroZ() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float dps = g.gyro.z * 57.2958; // rad/s -> deg/s
  return dps * 131.0;             // deg/s -> raw-equivalent LSB units
}

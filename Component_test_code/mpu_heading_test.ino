#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

float heading = 0.0;
float gyroBias = 0.0;

unsigned long lastTime;

void setup() {

  Serial.begin(115200);

  if (!mpu.begin()) {
    Serial.println("MPU6050 not found!");
    while (1);
  }

  Serial.println("Keep robot still...");
  delay(1000);

  // Calibrate gyro Z bias
  float sum = 0;

  for (int i = 0; i < 300; i++) {

    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    sum += g.gyro.z;

    delay(10);
  }

  gyroBias = sum / 300.0;

  heading = 0.0;
  lastTime = micros();

  Serial.println("Calibration Complete");
  Serial.println("Heading = 0");
}

void loop() {

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  unsigned long now = micros();
  float dt = (now - lastTime) / 1000000.0;
  lastTime = now;

  // Convert rad/s to deg/s
  float gyroZ = (g.gyro.z - gyroBias) * 180.0 / PI;

  heading += gyroZ * dt;

  Serial.print("Heading: ");
  Serial.print(heading, 2);
  Serial.println(" deg");

  delay(20);
}

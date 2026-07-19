#include <Wire.h>

const int MPU = 0x68;

float gyroZOffset = 0;
float heading = 0;

unsigned long lastTime;
bool stopped = false;

void setup() {
 Serial.begin(115200);
 Wire.begin();
 // Wake up MPU6050
 Wire.beginTransmission(MPU);
 Wire.write(0x6B);
 Wire.write(0);
 Wire.endTransmission(true);
 Serial.println("Keep the robot still...");
 delay(2000);
 // Calibrate gyro Z offset
 long sum = 0;
 const int samples = 1000;
  
 for (int i = 0; i < samples; i++) {
   sum += readGyroZ();
   delay(2);
 }
 gyroZOffset = (float)sum / samples;
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
 // Convert raw reading to degrees/sec
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

int16_t readGyroZ() {
 Wire.beginTransmission(MPU);
 Wire.write(0x47);   // GYRO_ZOUT_H
 Wire.endTransmission(false);
 Wire.requestFrom(MPU, 2, true);
 int16_t gz = Wire.read() << 8 | Wire.read();
 return gz;
}

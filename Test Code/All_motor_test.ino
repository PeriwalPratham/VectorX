#include <Servo.h>

#define DIR1 7
#define PWM1 6
#define SERVO_PIN 9

Servo steering;

const int SPEED = 255;
const int CENTER = 90;
const int LEFT = 70;
const int RIGHT = 110;

void setup() {
  pinMode(DIR1, OUTPUT);
  pinMode(PWM1, OUTPUT);

  steering.attach(SERVO_PIN);
  steering.write(CENTER);
}

// Move Forward (SWAPPED)
void forward() {
  steering.write(CENTER);
  digitalWrite(DIR1, LOW);
  analogWrite(PWM1, SPEED);
}

// Move Backward (SWAPPED)
void backward() {
  steering.write(CENTER);
  digitalWrite(DIR1, HIGH);
  analogWrite(PWM1, SPEED);
}

// Turn Left
void left() {
  steering.write(LEFT);
  digitalWrite(DIR1, LOW);
  analogWrite(PWM1, SPEED);
}

// Turn Right
void right() {
  steering.write(RIGHT);
  digitalWrite(DIR1, LOW);
  analogWrite(PWM1, SPEED);
}

// Stop
void stopMotor() {
  analogWrite(PWM1, 0);
  steering.write(CENTER);
}

// Straight
void straight() {
  steering.write(CENTER);
  digitalWrite(DIR1, LOW);
  analogWrite(PWM1, SPEED);
}

void loop() {

  forward();
  delay(2000);

  left();
  delay(2000);

  right();
  delay(2000);

  backward();
  delay(2000);

  stopMotor();
  delay(2000);
}

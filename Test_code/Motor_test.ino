const int PWM_PIN = 11;
const int DIR_PIN = 13;

int motorSpeed = 150;

void setup() {

  Serial.begin(115200);

  pinMode(PWM_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);

  analogWrite(PWM_PIN, 0);

  Serial.println();
  Serial.println("========== MOTOR TEST ==========");
  Serial.println("Automatic test starting...");
  Serial.println();
}

void loop() {

  // -----------------------------
  // Automatic Test
  // -----------------------------

  Serial.println("Forward @100");
  digitalWrite(DIR_PIN, HIGH);
  analogWrite(PWM_PIN, 100);
  delay(2000);

  Serial.println("Stop");
  analogWrite(PWM_PIN, 0);
  delay(1000);

  Serial.println("Forward @175");
  analogWrite(PWM_PIN, 175);
  delay(2000);

  Serial.println("Stop");
  analogWrite(PWM_PIN, 0);
  delay(1000);

  Serial.println("Reverse @150");
  digitalWrite(DIR_PIN, LOW);
  analogWrite(PWM_PIN, 150);
  delay(2000);

  Serial.println("Stop");
  analogWrite(PWM_PIN, 0);
  delay(1000);

  // -----------------------------
  // Manual Control
  // -----------------------------

  Serial.println();
  Serial.println("Waiting for command...");

  while (true) {

    if (Serial.available()) {

      char cmd = toupper(Serial.read());

      switch (cmd) {

        case 'F':
          digitalWrite(DIR_PIN, HIGH);
          analogWrite(PWM_PIN, motorSpeed);
          Serial.print("Forward  Speed = ");
          Serial.println(motorSpeed);
          break;

        case 'R':
          digitalWrite(DIR_PIN, LOW);
          analogWrite(PWM_PIN, motorSpeed);
          Serial.print("Reverse  Speed = ");
          Serial.println(motorSpeed);
          break;

        case 'S':
          analogWrite(PWM_PIN, 0);
          Serial.println("Motor Stopped");
          break;

        case '1':
          motorSpeed = 100;
          Serial.println("Speed = 100");
          break;

        case '2':
          motorSpeed = 150;
          Serial.println("Speed = 150");
          break;

        case '3':
          motorSpeed = 200;
          Serial.println("Speed = 200");
          break;

        case '4':
          motorSpeed = 255;
          Serial.println("Speed = 255");
          break;
      }
    }
  }
}


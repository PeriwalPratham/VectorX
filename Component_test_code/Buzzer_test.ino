/*
=========================================
BUZZER TEST

Hardware
---------
Arduino Uno
Passive/Active Buzzer

Pin
----
D4

Purpose
-------
- Verify buzzer wiring
- Play several beep patterns

Baud Rate
---------
115200
=========================================
*/

const int BUZZER_PIN = 4;

void beep(int frequency, int duration)
{
  tone(BUZZER_PIN, frequency);
  delay(duration);
  noTone(BUZZER_PIN);
  delay(100);
}

void setup()
{
  Serial.begin(115200);

  pinMode(BUZZER_PIN, OUTPUT);

  Serial.println();
  Serial.println("========================");
  Serial.println("BUZZER TEST");
  Serial.println("========================");
}

void loop()
{
  Serial.println("1000 Hz");
  beep(1000, 300);

  Serial.println("1500 Hz");
  beep(1500, 300);

  Serial.println("2000 Hz");
  beep(2000, 300);

  Serial.println("Double Beep");
  beep(1800, 150);
  beep(1800, 150);

  Serial.println("Long Beep");
  beep(1200, 1000);

  Serial.println("Waiting 3 seconds...");
  delay(3000);
}

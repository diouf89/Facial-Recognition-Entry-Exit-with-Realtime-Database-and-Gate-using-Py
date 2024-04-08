#include <Servo.h>

Servo myservo;  // create servo object to control a servo

void setup() {
  myservo.attach(3);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);  // initialize serial communication
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // read the incoming command

    if (command == '1') {
      myservo.write(90);  // turn the servo to 90 degrees
      delay(2000);        // wait for 5 seconds
      myservo.write(0);   // return the servo to its original position
    }
  }
}

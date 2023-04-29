/*
 Controlling a servo position using a potentiometer (variable resistor)
 by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>

 modified on 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Knob
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo

// int potpin = A0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  pinMode(2, INPUT);
}


void loop() {
  int i = 0;
  while(digitalRead(2) && i < (2*1000)){                  // sets the servo position according to the scaled value
                                         // waits for the servo to get there
    myservo.write(90);
    delay(1);
    i++;
  }
  myservo.write(0);
}

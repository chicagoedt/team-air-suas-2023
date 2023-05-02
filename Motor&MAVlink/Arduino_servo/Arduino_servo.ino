#include <Servo.h>

Servo myservo;  // create servo object to control a servo

#define Jet_pin 2
#define Ser_pin 9
#define Enc_pin 5

#define min_brk 60
#define max_brk 90

#define spool_diam .03 // in meters
float bot_pos;
int ser_pos;

float rots;
float bot_vel;

int deltat;
int prevt;
int newt;

void calc_vels(){
  int period = 0;
  for(int i = 0; i < 20;i++){
    period = period + pulseIn(Enc_pin, LOW);
  }
  period = period / 20;
  rots = 1/(period*18*10^6); 
  // new defintion converts period to frequency since 18 pulse = 1 rot and 10^6 usec = 1s

  bot_vel = rots * spool_diam *PI; // new definition
  return; 
}

void brake(int percent){
  if(percent <= 0 && ser_pos != 0){
    ser_pos = 0;
    myservo.write(min_brk - 5);
    return;
  }
  int new_pos = map(percent, 0, 100, min_brk, max_brk);

  if((new_pos >= .03*(ser_pos)) && (new_pos <= .03*(ser_pos)) ){
    myservo.write(new_pos);
    ser_pos = new_pos;
  }
  return;
}

void setup(){
  Serial.begin(9600);
  pinMode(Enc_pin, INPUT);
  pinMode(Jet_pin, INPUT);
  myservo.attach(Ser_pin);
  prevt = millis();
}

void loop(){
  newt = millis();
  deltat = (newt - prevt)/1000;
  prevt = newt;
  calc_vels();
  bot_pos += bot_vel * deltat;
  // IDK but figure out the way we want to restrict the speed of bottle
  if(bot_pos >= 10){
    brake(100);
  }
  // debug() ill implement later
}
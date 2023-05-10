#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time

servo = 18

def unbrake():
    pwm.set_servo_pulsewidth(servo, 500);
    return

def brake():
    pwm.set_servo_pulsewidth(servo, 1000);
    return

def clear():
    pwm.set_PWM_dutycycle(servo, 0)
    pwm.set_PWM_frequency(servo, 0)
    return

# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

clear()

pwm.set_PWM_frequency( servo, 50 )

time.sleep(1)

brake()

time.sleep(3)

unbrake()

time.sleep(4)

clear()


# turning off servo
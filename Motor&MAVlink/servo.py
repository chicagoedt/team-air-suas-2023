
import RPi.GPIO as GPIO
import time

output_pin = 33

def rotate(degrees):
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
    print("PWM running. Press CTRL+C to exit.")
    p = GPIO.PWM(output_pin, 50)
    left = 5
    neutral = 7.5
    right = 10
    p.ChangeDutyCycle(left) #1ms
    time.sleep(.5)
    p.ChangeDutyCycle(right) #2ms
    time.sleep(.5)
    p.stop()
    GPIO.cleanup()
    return




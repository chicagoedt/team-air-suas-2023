from gpiozero import Button
from gpiozero import RGBLED
from gpiozero import Servo
import board
import adafruit_tcs34725
from time import sleep

class Control:
    # constructor
    def __init__(self):
        self.button = Button(12)
        self.led = RGBLED(21, 20, 16)
        self.colorSensor = None
        try:
            i2c = board.I2C()
            self.colorSensor = adafruit_tcs34725.TCS34725(i2c)
        except:
            print("no color sensor connected")
        self.doorServo = Servo(14)
        self.pushServo = Servo(15)
        self.vacuumMotor = Servo(26)
        self.vacuumMotor.value = -1
        self.chamberServo = Servo(23)

    # set the color of the rgb leds
    def setRGB(self, rgb):
        self.led.color = (rgb[0]/255, rgb[1]/255, rgb[2]/255)  # rgb values must be between 0 and 1

    # read color from colorSensor
    def readColor(self):
        return self.colorSensor.color_rgb_bytes

    # reset all servos to the position zero
    def resetServos(self):
        self.doorServo.min()
        self.pushServo.min()
        sleep(0.5)
        self.doorServo.value = 0.1
        self.pushServo.max()
        sleep(0.5)
        self.doorServo.min()
        self.doorServo.min()
        self.pushServo.min()
        self.pushServo.min()

    # let ball fall into basket chamber
    def keepBall(self):
        # lever in
        self.pushServo.value = 0.6
        sleep(0.2)
        # vacuum off, door open
        self.setVacuumMotor(False)
        self.doorServo.value = 0.1
        sleep(0.5)
        # reset
        self.doorServo.min()
        self.pushServo.min()
        self.setVacuumMotor(True)

    # turn off the vacuum
    def dropBall(self):
        self.setVacuumMotor(False)
        sleep(1)
        self.setVacuumMotor(True)

    # turn vacuum on/off
    def setVacuumMotor(self, on):
        if on:
            self.vacuumMotor.value = 0.2
        else:
            self.vacuumMotor.value = -1


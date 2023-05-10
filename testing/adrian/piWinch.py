from gpiozero import Servo
from time import sleep

winch = Servo(14)
winch.max()
sleep(9)
winch.value = 0

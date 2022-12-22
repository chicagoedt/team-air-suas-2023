from gpiozero import Servo
from time import sleep

winch = Servo(14)
winch.max()
sleep(5)
winch.value = 0

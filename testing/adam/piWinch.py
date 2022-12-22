from gpiozero import Servo
from time import sleep

winch = Servo(14)
winch.min()
sleep(5)
winch.value = 0

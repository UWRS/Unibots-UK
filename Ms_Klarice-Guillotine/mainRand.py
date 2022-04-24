from Robot import Robot, Motor, Servo
import random
from time import sleep
import threading
import time

r = Robot(Motor(8, 10), Motor(16, 18), Servo(32))

def G():
	r.moveGuillotine(True)
	r.moveGuillotine(False)
	G()

threading.Thread(target=G).start()

b = True

s = time.time()

r.motor1.drive(80)
r.motor2.drive(80)
sleep(2.5)

while True:

	r.motor1.drive(100)
	r.motor2.drive(25)

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

class Servo:

	def __init__(self, pin):
		GPIO.setup(pin, GPIO.OUT)

		self.pwm = GPIO.PWM(pin, 50)

		self.pwm.start(0)

	# Drive the robot given the a speed
	# 
	# @param speed: Integer value between -100 and 100, where negative values are reverse
	def rotate(self, dir):

		cyc = 0
		if(dir):
			cyc = 5
		else:
			cyc = 10

		self.pwm.ChangeDutyCycle(cyc)

	def stop(self):
		self.pwm.ChangeDutyCycle(0)

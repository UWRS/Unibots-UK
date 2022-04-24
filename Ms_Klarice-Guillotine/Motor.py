import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class Motor:

	def __init__(self, in1, in2):
		GPIO.setup(in1, GPIO.OUT)
		GPIO.setup(in2, GPIO.OUT)

		self.dir1 = GPIO.PWM(in1, 1000)
		self.dir2 = GPIO.PWM(in2, 1000)

		self.dir1.start(0)
		self.dir2.start(0)

	# Drive the robot given the a speed
	# 
	# @param speed: Integer value between -100 and 100, where negative values are reverse
	def drive(self, speed):

		if(speed < -100):
			speed = -100
		if(speed > 100):
			speed = 100

		if(speed > 0):
			self.dir1.ChangeDutyCycle(0)
			self.dir2.ChangeDutyCycle(abs(speed))
		else:
			self.dir1.ChangeDutyCycle(abs(speed))
			self.dir2.ChangeDutyCycle(0)

	def stop(self):
		self.dir1.ChangeDutyCycle(0)
		self.dir2.ChangeDutyCycle(0)

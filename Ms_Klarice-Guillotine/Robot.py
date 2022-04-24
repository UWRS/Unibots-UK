import RPi.GPIO as GPIO
from time import sleep
import threading

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
        # @param speed: Integer value between -100 and 100, where negative valu$
        def drive(self, speed):

                if(speed < -100):
                        speed = -100
                if(speed > 100):
                        speed = 100

                if(speed < 0):
                        self.dir1.ChangeDutyCycle(0)
                        self.dir2.ChangeDutyCycle(abs(speed))

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


class Servo:

        def __init__(self, pin):
                GPIO.setup(pin, GPIO.OUT)

                self.pwm = GPIO.PWM(pin, 50)

                self.pwm.start(0)

        # Drive the robot given the a speed
        # 
        # @param speed: Integer value between -100 and 100, where negative valu$
        def rotate(self, dir):
                cyc = 0
                if(dir):
                        cyc = 5
                else:
                        cyc = 10

                self.pwm.ChangeDutyCycle(cyc)

        def stop(self):
                self.pwm.ChangeDutyCycle(0)


class Robot:

	GUILLOTINE_RAISED = True

	def __init__(self, m1, m2, servo):

		self.motor1 = m1
		self.motor2 = m2
		self.servo = servo

		self.guillotineState = not self.GUILLOTINE_RAISED
		threading.Thread(target=self.__calibrateGuillotine).start()

	def __calibrateGuillotine(self):
		self.servo.rotate(True)
		sleep(1)
		self.servo.stop()
		threading.Thread(target=self.moveGuillotine, args=(False,)).start()

	def moveGuillotine(self, dir):
		if((self.guillotineState == dir) == self.GUILLOTINE_RAISED):
			print("yes")
			self.servo.rotate(dir)
			sleep(0.5)
			self.servo.stop()
			self.guillotineState = not self.guillotineState

	def raiseGuillotine(self):
		threading.Thread(target=self.moveGuillotine, args=(False,)).start()

	def lowerGuillotine(self):
		threading.Thread(target=self.moveGuillotine, args=(True,)).start()

	def forward(self):
		self.motor1.drive(100)
		self.motor2.drive(100)

	def backward(self):
		self.motor1.drive(-100)
		self.motor2.drive(-100)

	def ts(self):
		self.motor1.drive(100)
		self.motor2.drive(-100)

	def stop(self):
		self.motor1.stop()
		self.motor2.stop()

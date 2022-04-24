import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

a1 = 8
a2 = 10
p = 32

GPIO.setup(a1, GPIO.OUT)
GPIO.setup(a2, GPIO.OUT)
GPIO.setup(p, GPIO.OUT)

pwm = GPIO.PWM(p, 100)
#pwm.start(0)

GPIO.output(a2, GPIO.HIGH)
GPIO.output(a1, GPIO.LOW)

pwm.start(0)

sleep(0.5)
print("start")
for i in range(0, 100):
	pwm.ChangeDutyCycle(i)
	sleep(0.1)

sleep(0.5)
print("cont")
for i in range(0, 100):
	pwm.ChangeDutyCycle(100-i)
	sleep(0.1)
print("end")

pwm.ChangeDutyCycle(0)

sleep(2)

GPIO.output(a1, GPIO.LOW)
GPIO.output(a2, GPIO.LOW)


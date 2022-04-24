import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

p = 32

GPIO.setmode(GPIO.BOARD)

GPIO.setup(p, GPIO.OUT)

pwm = GPIO.PWM(p, 50)
pwm.start(0)

pwm.ChangeDutyCycle(10)
sleep(1)
pwm.ChangeDutyCycle(5)
sleep(2)
pwm.ChangeDutyCycle(15)
sleep(1)

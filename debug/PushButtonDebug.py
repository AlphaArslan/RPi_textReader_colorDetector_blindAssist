import RPi.GPIO as GPIO
import time

trig1 = 2  # read text trigger
trig2 = 3  # detect color trigger

GPIO.setmode(GPIO.BCM)
GPIO.setup(trig1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(trig2, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    print("Push Button 1:\t\t" + str(GPIO.input(trig1)))
    print("Push Button 2:\t\t" + str(GPIO.input(trig2)))
    time.sleep(0.5)
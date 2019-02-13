import RPi.GPIO as GPIO
import time

DEBUG = False
CYCLES_NUM = 20

trig1 = 2  # read text trigger
trig2 = 3  # detect color trigger
s2 = 23
s3 = 24
signal = 25



def detect_color_from_sensor():
    if DEBUG is True:
        print("\nReading from Color Sensor IN HZ")
    # refer to sensor datasheet for deep understanding
    # reading red, s2:LOW s3:LOW
    GPIO.output(s2, GPIO.LOW)
    GPIO.output(s3, GPIO.LOW)
    time.sleep(0.3)
    # calculating time for CYCLES_NUM pulses
    start = time.time()
    for impulse_count in range(CYCLES_NUM):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    red = CYCLES_NUM / duration  # in Hz
    if DEBUG is True:
        print("Red Hz : " + str(red))


    # reading green, s2:HIGH s3:HIGH
    GPIO.output(s2, GPIO.HIGH)
    GPIO.output(s3, GPIO.HIGH)
    time.sleep(0.3)
    # calculating time for CYCLES_NUM pulses
    start = time.time()
    for impulse_count in range(CYCLES_NUM):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    green = CYCLES_NUM / duration  # in Hz
    if DEBUG is True:
        print("Green Hz : " + str(green))


    # reading blue, s2:LOW s3:HIGH
    GPIO.output(s2, GPIO.LOW)
    GPIO.output(s3, GPIO.HIGH)
    time.sleep(0.3)
    # calculating time for CYCLES_NUM pulses
    start = time.time()
    for impulse_count in range(CYCLES_NUM):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = CYCLES_NUM / duration  # in Hz
    if DEBUG is True:
        print("Blue Hz : " + str(blue))

    return red, green, blue


############# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(s2, GPIO.OUT)
GPIO.setup(s3, GPIO.OUT)
GPIO.setup(trig1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(trig2, GPIO.IN, pull_up_down=GPIO.PUD_UP)



print("White 1 , press when ready")
while GPIO.input(trig2) != 0:
    time.sleep(0.1)
white_red_1, white_green_1, white_blue_1 = detect_color_from_sensor()

print("White 2 , press when ready")
while GPIO.input(trig2) != 0:
    time.sleep(0.1)
white_red_2, white_green_2, white_blue_2 = detect_color_from_sensor()

print("White 3 , press when ready")
while GPIO.input(trig2) != 0 :
    time.sleep(0.1)
white_red_3, white_green_3, white_blue_3 = detect_color_from_sensor()

print("White 4 , press when ready")
while GPIO.input(trig2) != 0 :
    time.sleep(0.1)
white_red_4, white_green_4, white_blue_4 = detect_color_from_sensor()


print("black 1 , press when ready")
while GPIO.input(trig2) != 0 :
    time.sleep(0.1)
black_red_1, black_green_1, black_blue_1 = detect_color_from_sensor()

print("black 2 , press when ready")
while GPIO.input(trig2) != 0 :
    time.sleep(0.1)
black_red_2, black_green_2, black_blue_2 = detect_color_from_sensor()

print("black 3 , press when ready")
while GPIO.input(trig2) != 0 :
    time.sleep(0.1)
black_red_3, black_green_3, black_blue_3 = detect_color_from_sensor()

print("black 4 , press when ready")
while GPIO.input(trig2) != 0 :
    time.sleep(0.1)
black_red_4, black_green_4, black_blue_4 = detect_color_from_sensor()


print("\n\nCalibration Results:")

print("\tWhite:")
print("\t\tRed: "+str(white_red_1)+" , "+str(white_red_2)+" , "+str(white_red_3)+" , "+str(white_red_4))
print("\t\tGreen: "+str(white_green_1)+" , "+str(white_green_2)+" , "+str(white_green_3)+" , "+str(white_green_4))
print("\t\tBlue: "+str(white_blue_1)+" , "+str(white_blue_2)+" , "+str(white_blue_3)+" , "+str(white_blue_4))

print("\n\tBlack:")
print("\t\tRed: "+str(black_red_1)+" , "+str(black_red_2)+" , "+str(black_red_3)+" , "+str(black_red_4))
print("\t\tGreen: "+str(black_green_1)+" , "+str(black_green_2)+" , "+str(black_green_3)+" , "+str(black_green_4))
print("\t\tBlue: "+str(black_blue_1)+" , "+str(black_blue_2)+" , "+str(black_blue_3)+" , "+str(black_blue_4))


print("\n\nTuning Values:")
print("\tWhite: ( "+str((white_red_1+white_red_2+white_red_3+white_red_4)/4) +" , "+str((white_green_1+white_green_2+white_green_3+white_green_4)/4) +" , "+str((white_blue_1+white_blue_2+white_blue_3+white_blue_4)/4))
print("\tBlack: ( "+str((black_red_1+black_red_2+black_red_3+black_red_4)/4) +" , "+str((black_green_1+black_green_2+black_green_3+black_green_4)/4) +" , "+str((black_blue_1+black_blue_2+black_blue_3+black_blue_4)/4))


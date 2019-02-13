############# IMPORT
from gtts import gTTS
from PIL import Image
import RPi.GPIO as GPIO
import picamera
import pytesseract
import os
import time
import webcolors

############# Global
DEBUG = True
# constants
IMAGE_PATH = "testocr.png"
Mp3FileName = "speech.mp3"
CYCLES_NUM = 30

# pins
trig1 = 2  # read text trigger
trig2 = 3  # detect color trigger
s2 = 23
s3 = 24
signal = 25


############# Functions
def read_text():
    # capture the image and save it
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(IMAGE_PATH)
    im = Image.open(IMAGE_PATH)
    # extract the text
    text = pytesseract.image_to_string(im, lang='eng')
    if DEBUG is True:
        print("..\n")
        print(text)
        print("..\n")
    try:
        speech = gTTS(text=text, lang='en', slow=False)
    except AssertionError :
        print ("No Text in Image ..  Or Image not clear")
    else:
        # play sound
        speech.save(Mp3FileName)
        os.system("mpg123 " + Mp3FileName)


def detect_color_from_sensor():
    if DEBUG is True:
        print("\nReading from Color Sensor IN HEX")
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


def from_hz_to_RGB(r, g, b):
    if DEBUG is True:
        print("Converting Hz to RGB")
    # values got from calibration
    # red
    # 11000 Hz -----> 0   R
    # 27500 Hz -----> 255 R

    r = - 11000

    # 0    Hz -----> 0   R
    # 16500 Hz -----> 255 R
    r = (r / 16500) * 255


    # green
    # 13000 Hz -----> 0   G
    # 27500 Hz -----> 255 G

    g = - 13000

    # 0     Hz -----> 0   G
    # 14500 Hz -----> 255 G
    g = (g / 14500) * 255


    # blue
    # 15000 Hz -----> 0   B
    # 33000 Hz -----> 255 B

    b = - 15000

    # 0     Hz -----> 0   B
    # 18000 Hz -----> 255 B
    b = (b / 18000) * 255


    if DEBUG is True:
        print("Red RGB : " + str(int(r)))
        print("Green RGB : " + str(int(g)))
        print("Blue RGB : " + str(int(b)))
    return int(r), int(g), int(b)


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def rgb_to_str(r, g, b):
    if DEBUG is True:
        print("Converting RGB into a color")
    actual_name, closest_name = get_colour_name((r, g, b))
    if actual_name is None:
        return closest_name
    else:
        return actual_name


############# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(s2, GPIO.OUT)
GPIO.setup(s3, GPIO.OUT)
GPIO.setup(trig1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(trig2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

############# Loop
while True:
    # check for read text signal
    if GPIO.input(trig1) == 0:
        print("Read Text")
        read_text()

    # check for detect color signal
    if GPIO.input(trig2) == 0:
        print("Detect Color")
        r1, g1, b1 = detect_color_from_sensor()  # in Hz
        r1, g1, b1 = detect_color_from_sensor()  # in Hz
        r2, g2, b2 = detect_color_from_sensor()  # in Hz
        r3, g3, b3 = detect_color_from_sensor()  # in Hz
        r4, g4, b4 = detect_color_from_sensor()  # in Hz
        r5, g5, b5 = detect_color_from_sensor()  # in Hz
        r, g, b = (r1+r2+r3+r4+r5)/5, (g1+g2+g3+g4+g5)/5, (b1+b2+b3+b4+b5)/5
        r, g, b = from_hz_to_RGB(r, g, b)  # in RGB values
        color = rgb_to_str(r, g, b)
        print(color)
        speech = gTTS(text=color, lang='en', slow=False)
        speech.save(Mp3FileName)
        os.system("mpg123 " + Mp3FileName)
    print("Waiting for signal")
    time.sleep(0.1)
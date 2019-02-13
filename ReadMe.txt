This project is event triggered Text reader and color detector for the blind.
How it works:
	- there are two triggers (push buttons).
	- each trigger starts an objective:
		= first trigger starts text reader.
		= second trigger starts color detection.
---------------------------------------------------------------------------------
Setup Instructions:
	1- install tesseract-ocr " sudo apt-get install tesseract-ocr "
	2- install mpg123	 " sudo apt-get install mpg123 "
    3- Enable Rpi Camera " sudo raspi-config "
	4- install python modules:
		= sudo pip3 install setuptools --upgrade
		= sudo pip3 install pillow
		= sudo pip3 install pytesseract
		= sudo pip3 install gtts
		= sudo pip3 install webcolors
		= sudo pip3 install picamera
		= sudo pip3 install webcolors

	5- make sure you have internet connection or you will have trouble
	6- hopefully, now the program can start running fine and smooth
	7- report any error to me (+201207903371 whatsApp / arslan.alpha21@gmail.com)

----------------------------------------------------------------------------------
Hardware Instructions:
    1- TCS3200 color sensor is the one being used here.
       you better read the data sheet provided.
    2- a photo indicating circuit connection is provided.
       follow it carefully.
    3- two push buttons (i.e. triggers) is needed to trigger software events.
       the pins are pulled up, so connect the push buttons to GND, so that when closed,
       the pins read LOW status.
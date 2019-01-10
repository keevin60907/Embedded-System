import RPi.GPIO as GPIO
PIN_NO = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
GPIO.setup(PIN_NO, GPIO.OUT)
GPIO.output(PIN_NO, GPIO.LOW)


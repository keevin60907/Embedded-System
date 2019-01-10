import RPi.GPIO as GPIO
import time
import signal

PIN_NO = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PIN_NO, GPIO.OUT)

def beep(freq):
    breaktime = 1.0 / (freq * 2)
    GPIO.output(PIN_NO, GPIO.HIGH)
    time.sleep(breaktime)
    GPIO.output(PIN_NO, GPIO.LOW)
    time.sleep(breaktime)

def high(_signo, _stack_frame):
    GPIO.output(3, GPIO.HIGH)
    print('Set to high ...')
def low(_signo, _stack_frame):
    GPIO.output(3, GPIO.LOW)
    print('Set to low ...')

signal.signal(signal.SIGUSR1, high)
signal.signal(signal.SIGUSR2, low)


try:
    while True:
        beep(3)
except KeyboardInterrupt:
    GPIO.output(PIN_NO, GPIO.LOW)

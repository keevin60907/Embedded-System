import time
import RPi.GPIO as GPIO
import signal 

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
r = GPIO.PWM(18, 500)
g = GPIO.PWM(23, 500) 
b = GPIO.PWM(24, 500)



r.start(0)
g.start(0)
b.start(0)
def dim(r,g,b,color, f):
    breaktime = 1.0 / (f * 40)
    for dc in range(0, 101, 5):
        if color[0]:
            r.ChangeDutyCycle(dc)
        if color[1]:
            g.ChangeDutyCycle(dc)
        if color[2]:
            b.ChangeDutyCycle(dc)
        time.sleep(breaktime)
    for dc in range(100, -1, -5):
        if color[0]:
            r.ChangeDutyCycle(dc)
        if color[1]:
            g.ChangeDutyCycle(dc)
        if color[2]:
            b.ChangeDutyCycle(dc)
        time.sleep(breaktime)

FREQ = 0.5

def clean(_signo, _stack_frame):
    GPIO.cleanup()
    # print('Exit ...')
    exit(0)

signal.signal(signal.SIGTERM, clean)

try:
    while True:
        dim(r,g,b,(1,0,0), FREQ)
        dim(r,g,b,(0,1,0), FREQ)
        dim(r,g,b,(0,0,1), FREQ)
        dim(r,g,b,(1,1,0), FREQ)
        dim(r,g,b,(1,0,1), FREQ)
        dim(r,g,b,(0,1,1), FREQ)
        dim(r,g,b,(1,1,1), FREQ)
except KeyboardInterrupt:
    pass
r.stop()
g.stop()
b.stop()
GPIO.cleanup()

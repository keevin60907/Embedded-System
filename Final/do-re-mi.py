import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 50)
p.start(50)
def DoReMi(p):

    print('Do')
    p.ChangeFrequency(25)
    time.sleep(1)

    print('Re')
    p.ChangeFrequency(34)
    time.sleep(1)

    print('Me')
    p.ChangeFrequency(47)
    time.sleep(1)


try:
    while True:
        DoReMi(p)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()

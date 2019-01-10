import threading
import RPi.GPIO as GPIO
from queue import Queue
import os
import sys
import time
import signal
from functools import partial

class MyThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.event = args[0]
        self.quit = args[1]
        self.pins = args[2]
        self.daemon = True

class BeepThread(MyThread):
    def __init__(self, args):
        super().__init__(args)
        self.freq = args[3]
    def run(self):
        while not self.quit.is_set():
            self.event.wait()
            while self.event.is_set() and not self.quit.is_set():
                breaktime = 1.0 / (self.freq * 2)
                GPIO.output(self.pins[0], GPIO.HIGH)
                time.sleep(breaktime)
                GPIO.output(self.pins[0], GPIO.LOW)
                time.sleep(breaktime)

class LedThread(MyThread):
    def __init__(self, args):
        super().__init__(args)
        self.freq = args[3]
        self.color = args[4]
    def run(self):
        while not self.quit.is_set():
            self.event.wait()
            while self.event.is_set() and not self.quit.is_set():
                breaktime = 1.0 / (self.freq * 2)
                if not self.color.empty():
                    color = self.color.get()
                for i in range(3):
                    dc = int((255 - color[i]) * 100 / 255)
                    self.pins[i].ChangeDutyCycle(dc)
                time.sleep(breaktime)
                for i in range(3):
                    self.pins[i].ChangeDutyCycle(100)
                time.sleep(breaktime)

def cleanup(args, sig_no, frame):
    args['quitEvent'].set()    
    args['beepEvent'].set()
    args['ledEvent'].set()
    args['beepThread'].join()
    args['ledThread'].join()
    for c in args['rgb']:
        c.stop()
    print('signal {0} cleanup ...'.format(sig_no))
    GPIO.cleanup()


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pins = [19, 21, 23, 11]
for p in pins:
    GPIO.setup(p, GPIO.OUT)

rgb = [GPIO.PWM(19, 50), GPIO.PWM(23, 50), GPIO.PWM(21, 50)]
for c in rgb:
    c.start(0)
    c.ChangeDutyCycle(100)

quitEvent = threading.Event()

beepEvent = threading.Event()
beepThread = BeepThread([beepEvent, quitEvent, [11], 3])
beepThread.start()

color = Queue()
ledEvent = threading.Event()
ledThread = LedThread([ledEvent, quitEvent, rgb, 3, color])
ledThread.start()

args = {'quitEvent':quitEvent, 'beepEvent':beepEvent, 'ledEvent':ledEvent, 
    'beepThread':beepThread, 'ledThread':ledThread, 'rgb':rgb}
signal.signal(signal.SIGINT, partial(cleanup, args))
signal.signal(signal.SIGTERM, partial(cleanup, args))

while True:
    cmd = input('Enter cmd: ')
    cmds = cmd.split(' ')
    if cmds[0] == 'quit':
        quitEvent.set()
        beepEvent.set()
        ledEvent.set()
        beepThread.join()
        ledThread.join()
        for c in rgb:
            c.stop()
        GPIO.cleanup()
        exit(0)
    elif cmds[0] == 'beep': 
        if beepEvent.is_set():
            beepEvent.clear()
        else:
            beepEvent.set()

    elif cmds[0] == 'led':
        cmds = cmd.split(' ')
        if len(cmds) == 1:
            ledEvent.clear()
        else:
            r,g,b = int(cmds[1]), int(cmds[2]), int(cmds[3].strip())
            print(r,g,b)
            color.put([r,g,b])
            ledEvent.set()

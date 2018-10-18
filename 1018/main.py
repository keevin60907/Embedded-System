from __future__ import print_function
from adxl345 import ADXL345
from time import sleep

adxl345 = ADXL345()

while True:
    try:
        axes = adxl345.getAxes(True)
        print (" X = %.3fG, Y = %.3fG, Z = %.3fG \r" % ( axes["x"], axes["y"], axes["z"]), end=" ")
        sleep(0.005)
    except KeyboardInterrupt:
        break



from adxl345 import ADXL345

adxl345 = ADXL345()

axes = adxl345.getAxes(True)
print" X = %.3fG" % ( axes["x"])
print" Y = %.3fG" % ( axes["y"])
print" Z = %.3fG" % ( axes["z"])
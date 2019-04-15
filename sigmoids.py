#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
import matplotlib.pyplot as plt

"""
For each of the three values of V 2 that you used, fit a straight line to the plot of I 1 − I 2 as a function of V 1 − V 2 around the region where V 1 ≈ V 2 (i.e., where V 1 − V 2 ≈ 0). The slope of this line is approximately equal to the (incremental) differential-mode transconductance gain of the differential pair, which is formally given by [ EQUATION ].  Does the value of the differential-mode transconductance gain change significantly as V 2 changes?
"""


# Info about trials
Vbs = [.563, .563, .563, 1.076, 1.076, 1.076]
V2s = [2.497, 3.508, 4.49, 4.49, 3.508, 2.493]
fileNames = [(("data/T%d.I1.csv" % n), ("data/T%d.I2.csv" % n)) for n in range(6)]

# Import data
Vdms = [] #plural of Vdm
I1s = []
I2s = []

for name in fileNames:
  Vdm = []
  I1 = []
  I2 = []
  with open(name[0]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      Vdm += [float(row[0])]
      I1 += [float(row[1])] 
  Vdms += [Vdm]
  I1s += [I1]

  with open(name[1]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      I2 += [float(row[1])] 
  I2s += [I1]

Idiffs = np.array(I1) - np.array(I2)

print(Idiffs)

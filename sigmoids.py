#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
import matplotlib.pyplot as plt

"""
For each of the three values of V 2 that you used, fit a straight line to the plot of I 1 − I 2 as a function of V 1 − V 2 around the region where V 1 ≈ V 2 (i.e., where V 1 − V 2 ≈ 0). The slope of this line is approximately equal to the (incremental) differential-mode transconductance gain of the differential pair, which is formally given by [ EQUATION ].  Does the value of the differential-mode transconductance gain change significantly as V 2 changes?
"""

def clip(xs, ys, xbounds, ybounds):
  pairs = [(x, y) for (x, y) in zip(xs, ys) if (xbounds[0] <= x) and (x <= xbounds[1]) and (ybounds[0] <= y) and (y <= ybounds[1])]
  out = list(zip(*pairs))
  return np.array(out[0]), np.array(out[1])

def clipDomain(xs, ys, xbounds): # Useful if y-data is not numbers
  pairs = [(x, y) for (x,y) in zip(xs, ys) if (xbounds[0] <= x) and (x <= xbounds[1])]
  out = list(zip(*pairs))
  return np.array(out[0]), np.array(out[1])


# Info about trials
Vbs = [.563, .563, .563, 1.076, 1.076, 1.076]
V2s = [2.497, 3.508, 4.49, 4.49, 3.508, 2.493]
fileNames = [(("data/T%d.I1.csv" % n), ("data/T%d.I2.csv" % n)) for n in range(6)]

# Import data
Vdms = [] #plural of Vdm
I1s = []
I2s = []

for (i, name) in zip(range(6), fileNames):
  Vdm = []
  I1 = []
  I2 = []
  with open(name[0]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      Vdm += [float(row[0])]
      I1 += [float(row[1])] 

  with open(name[1]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      I2 += [float(row[1])] 

  # Vdm, Is = clipDomain(Vdm, zip(I1, I2), (-0.3,0.1) if i<3 else (-0.75, 0.5))
  # I1, I2 = list(zip(*Is))

  Vdms += [Vdm]
  I1s += [I1]
  I2s += [I2]

Idiffs = np.array(I1s) - np.array(I2s)

# Do fits
ms, bs, Vts, Its = [], [], [], []
for (Vdm, Idiff) in zip(Vdms, Idiffs):
  # Find where the sign changes.  Finding where the derivative hits 0 would also work but this seems more robust.
  crossing = int(np.mean(np.arange(len(Idiff)-1)[np.diff(np.sign(Idiff)) != 0]))
  domain = round(len(Vdm) * 0.005)
  # bounds = (round(len(Vdm) * 0.45), round(len(Vdm) * 0.55)) # Pick out the middle bit
  bounds = (crossing-domain, crossing+domain)
  m, b = np.polyfit(Vdm[bounds[0]:bounds[1]], Idiff[bounds[0]:bounds[1]], 1) # Do the fit
  It = m*np.array(Vdm) + b # Make theoretical data
  Vt, It = clip(Vdm, It, (-np.inf, np.inf), (min(Idiff), max(Idiff)))

  ms += [m]
  bs += [b]
  Vts += [Vt]
  Its += [It]


for (V2, Vb, m, b) in zip(V2s, Vbs,  ms, bs):
  print("V2 = %g, Vb= %g, m = %g, b = %g" % (V2, Vb, m, b))

# Plot things
fig = plt.figure(figsize=(8,6))
ax = plt.subplot(111)
colors = ['r','g','b','b','g','r']

# First, the ones with lower Vb
for (color, V2, Vdm, Vt, Idiff, It, m, b) in list(zip(colors, V2s, Vdms, Vts, Idiffs, Its, ms, bs))[:3]:
  ax.plot(Vdm, Idiff, color + '.', markersize=2, label="Differential current (V2 = %g)" % V2)
  ax.plot(Vt, It, color + '-', markersize=1, label="Theoretical fit (V2 = %g, slope = %g ℧)" % (V2, m))


plt.title("Differential current (Vb = %g)" % Vbs[0])
plt.xlabel("Differential voltage (V)")
plt.ylabel("Differential current (A)")
ax.legend()
plt.savefig("sigmoid-low-vb.pdf")
plt.cla()

# Next, the ones with higher Vb
for (color, V2, Vdm, Vt, Idiff, It, m, b) in list(zip(colors, V2s, Vdms, Vts, Idiffs, Its, ms, bs))[3:]:
  ax.plot(Vdm, Idiff, color + '.', markersize=2, label="Differential current (V2 = %g)" % V2)
  ax.plot(Vt, It, color + '-', markersize=1, label="Theoretical fit (V2 = %g, slope = %g ℧)" % (V2, m))

plt.title("Differential current (Vb = %g)" % Vbs[3])
plt.xlabel("Differential voltage (V)")
plt.ylabel("Differential current (A)")
ax.legend()
plt.savefig("sigmoid-high-vb.pdf")
plt.cla()

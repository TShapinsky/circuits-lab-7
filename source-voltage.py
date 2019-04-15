#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
import matplotlib.pyplot as plt

"""
include a plot showing the common-source node voltage, V , as a function of V 1 − V 2 for all three values of V 2 . How does the value of V change as V 1 goes from below V 2 to above it?
"""

def clip(xs, ys, xbounds, ybounds):
  pairs = [(x, y) for (x, y) in zip(xs, ys) if (xbounds[0] <= x) and (x <= xbounds[1]) and (ybounds[0] <= y) and (y <= ybounds[1])]
  out = list(zip(*pairs))
  return np.array(out[0]), np.array(out[1])

def clip_range(xs, ys, bounds):
  return clip(xs, ys, (-np.inf, np.inf), bounds)

def fit(xs, ys, model, initial_params):
  def err_f(params): return np.mean(np.power(np.log(ys) - np.log(model(xs, params)), 2))
  res = minimize(err_f, x0 = initial_params, method='Nelder-Mead')
  print(res)
  return res.x


# Info about trials
Vbs = [.563, .563, .563, 1.076, 1.076, 1.076]
V2s = [2.497, 3.508, 4.49, 4.49, 3.508, 2.493]
fileNames = ["data/T%d.V.csv" % n for n in range(6)]

# Import data
Vdms = [] #plural of Vdm
Vs = []

for name in fileNames:
  Vdm = []
  V = []
  with open(name) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      Vdm += [float(row[0])]
      V += [float(row[1])] 
  Vdms += [Vdm]
  Vs += [V]


# Plot things
fig = plt.figure(figsize=(8,6))
ax = plt.subplot(111)

# First, the ones with lower Vb
for (color, V2, Vdm, V) in zip(['b','g','r'], V2s, Vdms, Vs[:3]):
  ax.plot(Vdm, V, color + '.', markersize=1, label="V2 = %g V" % V2)
plt.title("Common source node voltage (Vb = %g V)" % Vbs[0])
plt.xlabel("Differential voltage (V)")
plt.ylabel("Common-source voltage (V)")
plt.grid(True)
ax.legend()
plt.savefig("source-voltage-low-vb.pdf")
plt.cla()

# Now higher Vb.  Reverse colors so they match
for (color, V2, Vdm, V) in zip(['r','g','b'], V2s[3:], Vdms[3:], Vs[3:]):
  ax.plot(Vdm, V, color + '.', markersize=1, label="V2 = %g V" % V2)
plt.title("Common source node voltage (Vb = %g V)" % Vbs[3])
plt.xlabel("Differential voltage (V)")
plt.ylabel("Common-source voltage (V)")
plt.grid(True)
ax.legend()
plt.savefig("source-voltage-high-vb.pdf")
plt.cla()

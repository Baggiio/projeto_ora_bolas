import numpy as np
from math import *
import matplotlib.pyplot as plt

lt = []
lx = []
ly = []

with open("trajetoria.txt", "r") as tj:
    lines = tj.readlines()
    for i in range(1, len(lines)):
        l = lines[i].strip("\n").split("\t")
        for i in range(len(l)):
            l[i] = float(l[i].replace(",", "."))
        if l[0] >= 0 and l[1] >= 0 and l[2] >= 0:
            lt.append(l[0])
            lx.append(l[1])
            ly.append(l[2])
        
rx = []
for t in lt:
    rx.append(6-2.8*t)

ry = []
for t in lt:
    ry.append(2-0*t)

fig, ax = plt.subplots()
ax.plot(lx, ly)
ax.plot(rx, ry)
plt.show()
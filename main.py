import numpy as np
from math import *
import matplotlib.pyplot as plt

lt = []
lx = []
ly = []
nt = []
nx = []
ny = []

# sx = float(input("Posição inicial do robô no eixo x: "))
# sy = float(input("Posição inicial do robô no eixo y: "))
sx = 5
sy = 3

with open("trajetoria2.txt", "r") as tj:
    lines = tj.readlines()
    for i in range(1, len(lines)):
        l = lines[i].strip("\n").split("\t")
        for i in range(len(l)):
            l[i] = float(l[i].replace(",", "."))
        if l[0] >= 0 and l[1] >= 0 and l[2] >= 0:
            nt.append(l[0])
            nx.append(l[1])
            ny.append(l[2])
        if l[0] >= 0 and (l[1] >= 0 and l[1] <= 9) and (l[2] >= 0 and l[2] <= 6):
            lt.append(l[0])
            lx.append(l[1])
            ly.append(l[2])
fx = np.polyfit(nt, nx, 3).tolist()
fy = np.polyfit(nt, ny, 2).tolist()

fdx = np.polyder(fx).tolist()
fdy = np.polyder(fy).tolist()

vx = []
vy = []

for a in np.linspace(-2.8, 2.8, num=2*len(lt)):
    bmais = sqrt((196/25)-a**2)
    bmenos = -(sqrt((196/25)-a**2))
    for i in range(len(lt)):
        #x1 = (fx[0]*t**3 + fx[1]*t**2 + fx[2]*t + fx[3])
        x2 = (sx + a*lt[i])

        #y1 = (fy[0]*t**2 + fx[1]*t**2 + fx[2])
        y2 = (sy + bmais*lt[i])
        y3 = (sy + bmenos*lt[i])

        if abs(lx[i]-x2) <= 0.025 and x2 >= 0:
            if abs(ly[i]-y2) <= 0.025 and y2 >= 0:
                vx.append(a)
                vy.append(bmais)
                tempo = lt[i]
            elif abs(ly[i]-y3) <= 0.025 and y3 >= 0:
                vx.append(a)
                vy.append(bmenos)
                tempo = lt[i]
            else:
                pass

vxf = sum(vx)/len(vx)
vyf = sum(vy)/len(vy)
print("Vx = %f, Vy = %f, Tempo = %f" % (vxf, vyf, tempo))

rx = []
rx.append(sx)
rx.append(sx + vxf*tempo)

ry = []
ry.append(sy)
ry.append(sy + vyf*tempo)

ix = []
for i in range(len(lt)):
    if lt[i] == tempo:
        break
    else:
        ix.append(lx[i])

iy = []
for i in range(len(lt)):
    if lt[i] == tempo:
        break
    else:
        iy.append(ly[i])

fig, ax1 = plt.subplots()
# ax1.plot(ix, iy)
ax1.plot(lx, ly)
ax1.plot(rx, ry, marker = 'o', color = 'red')
ax1.text(rx[0] - rx[0]/2, ry[0] + 0.2, "Robô (s0)", fontsize=10, color="red")
ax1.text(rx[1] + 0.3, ry[1] - 0.1, ("Ponto de Interceptação (t = %.2f)" % tempo), fontsize=10, color="red")
ax1.plot([0, 0, 9, 9, 0], [0, 6, 6, 0, 0], color = 'black')
ax1.set(title = "Trajetória de interceptação entre robô e bola", xlabel = "x (m)", ylabel = "y (m)")
plt.grid(linestyle='--')
plt.savefig("trajetoria_de_interceptacao.png")

fig, ax2 = plt.subplots()
ax2.plot(nt, nx)
ax2.plot([lt[0], tempo], rx, marker = 'o', color = 'red')
ax2.set(title = "Posição x da bola e do robô pelo tempo", xlabel = "t (s)", ylabel = "x (m)")
plt.grid(linestyle='--')
plt.savefig("posicao_x_tempo.png")

fig, ax3 = plt.subplots()
ax3.plot(nt, ny)
ax3.plot([lt[0], tempo], ry, marker = 'o', color = 'red')
ax3.set(title = "Posição y da bola e do robô pelo tempo", xlabel = "t (s)", ylabel = "y (m)")
plt.grid(linestyle='--')
plt.savefig("posicao_y_tempo.png")
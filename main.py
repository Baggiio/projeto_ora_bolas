import numpy as np
from math import *
import matplotlib.pyplot as plt
from alive_progress import alive_bar

# Incializa as listas vazias para armazenar os valores de t, x e y
lt = []
lx = []
ly = []
nt = []
nx = []
ny = []

# Definição das constantes de posição inicial
# sx = float(input("Posição inicial do robô no eixo x: "))
# sy = float(input("Posição inicial do robô no eixo y: "))
sx = 22
sy = 7

# Abre o arquivo de entrada e lê os valores de t, x e y
with open("trajetorias/trajetoria.txt", "r") as tj:
    lines = tj.readlines()
    for i in range(1, len(lines)):
        l = lines[i].strip("\n").split("\t")
        for i in range(len(l)):
            l[i] = float(l[i].replace(",", "."))
        if l[0] >= 0 and l[1] >= 0 and l[2] >= 0:
            lt.append(l[0])
            lx.append(l[1])
            ly.append(l[2])
        # if l[0] >= 0 and (l[1] >= 0 and l[1] <= 9) and (l[2] >= 0 and l[2] <= 6):
        #     lt.append(l[0])
        #     lx.append(l[1])
        #     ly.append(l[2])

# Aproxima uma função polinomial para os valores de x e y
fx = np.polyfit(lt, lx, 3).tolist()
fy = np.polyfit(lt, ly, 2).tolist()

# Deriva a função polinomial para obter a velocidade
fdx = np.polyder(fx).tolist()
fdy = np.polyder(fy).tolist()

# Deriva a função polinomial para obter a aceleração
fddx = np.polyder(fdx).tolist()
fddy = np.polyder(fdy).tolist()

# Inicializa as listas vazias para armazenar os valores de Vx e Vy
vx = []
vy = []

# Testa diversos valores de Vx e Vy para encontrar a interceptação em menor tempo

print("Realizando testes...")
with alive_bar(50*len(lt)) as bar:
    wait = 0
    for a in np.linspace(-2.8, 2.8, num=50*len(lt)):
        bar()
        bmais = sqrt((196/25)-a**2)
        bmenos = -(sqrt((196/25)-a**2))
        if wait == 0:
            for i in range(len(lt)):
                #x1 = (fx[0]*t**3 + fx[1]*t**2 + fx[2]*t + fx[3])
                x2 = (sx + a*lt[i])

                #y1 = (fy[0]*t**2 + fx[1]*t**2 + fx[2])
                y2 = (sy + bmais*lt[i])
                y3 = (sy + bmenos*lt[i])

                if abs(lx[i]-x2) <= 0.05 and x2 >= 0:
                    if abs(ly[i]-y2) <= 0.05 and y2 >= 0:
                        if x2 > 9 or y2 > 6:
                            print("O robô deverá esperar a bola retornar ao campo.")
                            for j in range(i, len(lt)):
                                if lx[j] <= 9 and ly[j] <= 6:
                                    waitx = lx[j]
                                    waity = ly[j]
                                    print(waitx)
                                    print(waity)
                                    break
                            wait = 1
                        vx.append(a)
                        vy.append(bmais)
                        tempo = lt[i]
                    elif abs(ly[i]-y3) <= 0.05 and y3 >= 0:
                        if x2 > 9 or y2 > 6:
                            print("O robô deverá esperar a bola retornar ao campo.")
                            for j in range(i, len(lt)):
                                if lx[j] <= 9 and ly[j] <= 6:
                                    waitx = lx[j]
                                    waity = ly[j]
                                    print(waitx)
                                    print(waity)
                                    break
                            wait = 1
                        vx.append(a)
                        vy.append(bmenos)
                        tempo = lt[i]
                    else:
                        pass
        else:
            for i in range(len(lt)):
                #x1 = (fx[0]*t**3 + fx[1]*t**2 + fx[2]*t + fx[3])
                x2 = (sx + a*lt[i])

                #y1 = (fy[0]*t**2 + fx[1]*t**2 + fx[2])
                y2 = (sy + bmais*lt[i])
                y3 = (sy + bmenos*lt[i])

                if abs(waitx-x2) <= 0.05 and x2 >= 0:
                    if abs(waity-y2) <= 0.05 and y2 >= 0:
                        vx.append(a)
                        vy.append(bmais)
                        tempo = lt[i]
                    elif abs(waity-y3) <= 0.05 and y3 >= 0:
                        vx.append(a)
                        vy.append(bmenos)
                        tempo = lt[i]
                    else:
                        pass

# Tira a média dos valores encontrados para Vx e Vy
vxf = sum(vx)/len(vx)
vyf = sum(vy)/len(vy)
print("Ponto de interceptação no menor tempo encontrado!")
print("A interceptação ocorrerá no instante t = %.2f." % tempo)
print("Para isso, o robô deve utilizar uma velocidade de Vx = %.2f e Vy = %.2f." % (vxf, vyf))

# Cria a trajetória x do robô
rx = []
rx.append(sx)
rx.append(sx + vxf*tempo)

# Cria a trajetória y do robô
ry = []
ry.append(sy)
ry.append(sy + vyf*tempo)

# Cria a trajetória x da bola até o momento de interceptação
ix = []
for i in range(len(lt)):
    if lt[i] == tempo:
        break
    else:
        ix.append(lx[i])

# Cria a trajetória y da bola até o momento de interceptação
iy = []
for i in range(len(lt)):
    if lt[i] == tempo:
        break
    else:
        iy.append(ly[i])

# Cria a curva de velocidade x da bola
vbx = []
for i in range(len(lt)):
    vbx.append(fdx[0]*lt[i]**2 + fdx[1]*lt[i] + fdx[2])

# Cria a curva de velocidade y da bola
vby = []
for i in range(len(lt)):
    vby.append(fdy[0]*lt[i] + fdy[1])

# Cria a curva de aceleração x da bola
abx = []
for i in range(len(lt)):
    abx.append(fddx[0]*lt[i] + fddx[1])

# Cria a curva de aceleração y da bola
aby = []
for i in range(len(lt)):
    aby.append(fddy[0])

# Plota o gráfico das trajetórias no plano
fig, ax1 = plt.subplots()
# ax1.plot(ix, iy)
ax1.plot(lx, ly, label="Bola", marker = 'o', markevery=[1])
ax1.plot(rx, ry, marker = 'o', color = 'red', label="Robô")
ax1.annotate('Robô (Inicial)', (rx[0] + 0.3, ry[0]), color = 'red')
ax1.annotate(("Interceptação (t = %.2f)" % tempo), (rx[1] + 0.3, ry[1] - 0.1), color = 'red')
# ax1.text(rx[0] + 0.3, ry[0] - 0.1, "Robô (inicial)", fontsize=10, color="red")
# ax1.text(rx[1] + 0.3, ry[1] - 0.1, ("Interceptação (t = %.2f)" % tempo), fontsize=10, color="red")
ax1.plot([0, 0, 9, 9, 0], [0, 6, 6, 0, 0], color = 'green', label="Campo")
ax1.set(title = "Trajetória do robô e da bola no campo", xlabel = "x (m)", ylabel = "y (m)")
ax1.minorticks_on()
ax1.legend()
ax1.grid(which='both')
ax1.grid(which='minor', alpha=0.2)
ax1.grid(which='major', alpha=0.5)
plt.tight_layout()
plt.savefig("results/trajetoria_de_interceptacao.png", dpi=200)

# Plota a trajetória x da bola e do robô pelo tempo
fig, ax2 = plt.subplots()
ax2.plot(lt, lx, label="Bola")
ax2.plot([lt[0], tempo], rx, marker = 'o', color = 'red', label="Robô")
ax2.text(tempo + 0.5, rx[1] - 0.1, ("Interceptação (t = %.2f)" % tempo), fontsize=10, color="red")
ax2.set(title = "Posição x da bola e do robô em função do tempo", xlabel = "t (s)", ylabel = "x (m)")
ax2.minorticks_on()
ax2.legend()
ax2.grid(which='both')
ax2.grid(which='minor', alpha=0.2)
ax2.grid(which='major', alpha=0.5)
plt.tight_layout()
plt.savefig("results/posicao_x_tempo.png", dpi=200)

# Plota a trajetória y da bola e do robô pelo tempo
fig, ax3 = plt.subplots()
ax3.plot(lt, ly, label="Bola")
ax3.plot([lt[0], tempo], ry, marker = 'o', color = 'red', label="Robô")
ax3.text(tempo + 0.5, ry[1] - 0.1, ("Interceptação (t = %.2f)" % tempo), fontsize=10, color="red")
ax3.set(title = "Posição y da bola e do robô em função do tempo", xlabel = "t (s)", ylabel = "y (m)")
ax3.minorticks_on()
ax3.legend()
ax3.grid(which='both')
ax3.grid(which='minor', alpha=0.2)
ax3.grid(which='major', alpha=0.5)
plt.tight_layout()
plt.savefig("results/posicao_y_tempo.png", dpi=200)

# Plota a velocidade x da bola e do robô pelo tempo
fig, ax4 = plt.subplots()
ax4.plot(lt, vbx, label="Bola")
ax4.plot([lt[0], lt[-1]], [vxf, vxf], color = 'red', label="Robô")
ax4.set(title = "Velocidade x da bola e do robô em função do tempo", xlabel = "t (s)", ylabel = "Vx (m/s)")
ax4.minorticks_on()
ax4.legend()
ax4.grid(which='both')
ax4.grid(which='minor', alpha=0.2)
ax4.grid(which='major', alpha=0.5)
plt.tight_layout()
plt.savefig("results/velocidade_x_tempo.png", dpi=200)

# Plota a velocidade y da bola e do robô pelo tempo
fig, ax5 = plt.subplots()
ax5.plot(lt, vby, label="Bola")
ax5.plot([lt[0], lt[-1]], [vyf, vyf], color = 'red', label="Robô")
ax5.set(title = "Velocidade y da bola e do robô em função do tempo", xlabel = "t (s)", ylabel = "Vy (m/s)")
ax5.minorticks_on()
ax5.legend()
ax5.grid(which='both')
ax5.grid(which='minor', alpha=0.2)
ax5.grid(which='major', alpha=0.5)
plt.tight_layout()
plt.savefig("results/velocidade_y_tempo.png", dpi=200)

# Plota a aceleração x da bola e do robô pelo tempo
fig, ax6 = plt.subplots()
ax6.plot(lt, abx, label="Bola")
ax6.plot([lt[0], lt[-1]], [0, 0], color = 'red', label="Robô")
ax6.set(title = "Aceleração x da bola e do robô em função do tempo", xlabel = "t (s)", ylabel = "Ax (m/s²)")
ax6.minorticks_on()
ax6.legend()
ax6.grid(which='both')
ax6.grid(which='minor', alpha=0.2)
ax6.grid(which='major', alpha=0.5)
plt.tight_layout()
plt.savefig("results/aceleracao_x_tempo.png", dpi=200)

# Plota a aceleração y da bola e do robô pelo tempo
fig, ax7 = plt.subplots()
ax7.plot(lt, aby, label="Bola")
ax7.plot([lt[0], lt[-1]], [0, 0], color = 'red', label="Robô")
ax7.set(title = "Aceleração y da bola e do robô em função do tempo", xlabel = "t (s)", ylabel = "Ay (m/s²)")
ax7.minorticks_on()
ax7.legend()
ax7.grid(which='both')
ax7.grid(which='minor', alpha=0.2)
ax7.grid(which='major', alpha=0.5)
plt.tight_layout()
plt.savefig("results/aceleracao_y_tempo.png", dpi=200)
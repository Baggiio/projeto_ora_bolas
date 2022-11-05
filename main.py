import numpy as np
from math import *
import matplotlib.pyplot as plt
import os
from alive_progress import alive_bar
from tkinter import *
from customtkinter import *
from PIL import ImageTk, Image
from zoom import Zoom_Advanced

def interceptacao(sx, sy, arquivo):

    # Incializa as listas vazias para armazenar os valores de t, x e y
    lt = []; lx = []; ly = []
    nt = []; nx = []; ny = []

    # Abre o arquivo de entrada e lê os valores de t, x e y
    with open(("trajetorias/%s.txt" % arquivo), "r") as tj:
        lines = tj.readlines()
        for i in range(1, len(lines)):
            l = lines[i].strip("\n").split("\t")
            for i in range(len(l)):
                l[i] = float(l[i].replace(",", "."))
            if l[0] >= 0 and l[1] >= 0 and l[2] >= 0:
                lt.append(l[0])
                lx.append(l[1])
                ly.append(l[2])
            if l[0] >= 0 and (l[1] >= 0 and l[1] <= 9) and (l[2] >= 0 and l[2] <= 6):
                nt.append(l[0])
                nx.append(l[1])
                ny.append(l[2])

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
    tempos = []
    tempos_chegada = []

    # Incializa a variável de controle da espera pela bola
    wait = 0
    found = 0

    # Testa diversos valores de Vx e Vy para encontrar a interceptação em menor tempo
    print("Realizando testes...")
    values = np.linspace(-2.8, 2.8, num=10000)
    update_progress(0)
    progress = 0
    for c in range(10000):
        if c % 500 == 0:
            progress += 0.05
            update_progress(progress)
        a = values[c]
        bmais = sqrt((196/25)-a**2)
        bmenos = -(sqrt((196/25)-a**2))
        if wait == 0:
            for i in range(len(lt)):
                x1 = (sx + a*lt[i])
                y1 = (sy + bmais*lt[i])
                y2 = (sy + bmenos*lt[i])

                if abs(lx[i]-x1) <= 0.06 and x1 >= 0:
                    if abs(ly[i]-y1) <= 0.06 and y1 >= 0:
                        if x1 > 9 or y1 > 6:
                            for j in range(i, len(lt)):
                                if lx[j] <= 9 and ly[j] <= 6:
                                    waitj = j
                                    tempos.append(lt[j])
                                    wait = 1
                                    break
                        else:
                            vx.append(a)
                            vy.append(bmais)
                            tempos.append(lt[i])
                            found = 1
                    elif abs(ly[i]-y2) <= 0.06 and y2 >= 0:
                        if x1 > 9 or y2 > 6:
                            for j in range(i, len(lt)):
                                if lx[j] <= 9 and ly[j] <= 6:
                                    waitj = j
                                    tempos.append(lt[j])
                                    wait = 1
                                    break
                        else:
                            vx.append(a)
                            vy.append(bmenos)
                            tempos.append(lt[i])
                            found = 1
                    else:
                        pass
        else:
            break
    if wait == 1:
        update_progress(0)
        for c in range(10000):
            if c % 500 == 0:
                progress += 0.05
                update_progress(progress)
            a = values[c]
            bmais = sqrt((196/25)-a**2)
            bmenos = -(sqrt((196/25)-a**2))
            for i in range(len(lt)):
                x1 = (sx + a*lt[i])
                y1 = (sy + bmais*lt[i])
                y2 = (sy + bmenos*lt[i])

                if abs(lx[waitj+2]-x1) <= 0.04 and x1 >= 0:
                    if abs(ly[waitj+2]-y1) <= 0.04 and y1 >= 0:
                        vx.append(a)
                        vy.append(bmais)
                        tempos_chegada.append(lt[i])
                        found = 1
                    elif abs(ly[waitj+2]-y2) <= 0.04 and y2 >= 0:
                        vx.append(a)
                        vy.append(bmenos)
                        tempos_chegada.append(lt[i])
                        found = 1
                    else:
                        pass

    if found == 0:
        wait = 0
        tempos = []
        bx = lx[-1]
        by = ly[-1]
        tg = abs((by-sy))/abs((bx-sx))
        ang = atan(tg)
        if by > sy:
            if bx > sx:
                vx.append((np.cos(ang)*2.8))
                vy.append((np.sin(ang)*2.8))
            else:
                vx.append(-(np.cos(ang)*2.8))
                vy.append((np.sin(ang)*2.8))
        else:
            if bx > sx:
                vx.append((np.cos(ang)*2.8))
                vy.append(-(np.sin(ang)*2.8))
            else:
                vx.append(-(np.cos(ang)*2.8))
                vy.append(-(np.sin(ang)*2.8))
        tempos.append(abs((bx-sx)/(np.cos(ang)*2.8)))

    # Tira a média dos valores encontrados para Vx e Vy
    vxf = sum(vx)/len(vx)
    vyf = sum(vy)/len(vy)
    tempo = (sum(tempos)/len(tempos)) - (0.0965/2.8)
    if wait == 1:
        tempo_chegada = (sum(tempos_chegada)/len(tempos_chegada))

    # Exibe os resultados encontrados
    print("Ponto de interceptação no menor tempo encontrado!")
    if wait == 1:
        print("O robô chegará no instante t = %.2f e deverá esperar a bola retornar ao campo." % tempo_chegada)
    print("A interceptação ocorrerá no instante t = %.2f." % tempo)
    print("Para isso, o robô deve utilizar uma velocidade de Vx = %.2f e Vy = %.2f." % (vxf, vyf))

    # Cria a trajetória x do robô
    rx = []
    rx.append(sx)
    if wait == 0:
        rx.append(sx + vxf*(tempo-0.005))
    else:
        rx.append(sx + vxf*tempo_chegada)

    # Cria a trajetória y do robô
    ry = []
    ry.append(sy)
    if wait == 0:
        ry.append(sy + vyf*(tempo-0.005))
    else:
        ry.append(sy + vyf*tempo_chegada)

    # Cria a trajetória do raio de interceptação
    rix = []
    riy = []
    if wait == 0:
        rix.append(sx + vxf*tempo)
        rix.append(sx + vxf*(tempo + (0.0965/2.8)))
        riy.append(sy + vyf*tempo)
        riy.append(sy + vyf*(tempo + (0.0965/2.8)))
    else:
        rix.append(lx[waitj+1])
        rix.append(lx[waitj+2])
        riy.append(ly[waitj+1])
        riy.append(ly[waitj+2])

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
    if wait == 0:
        ax1.plot(nx, ny, label="Bola", marker = 'o', markevery=[0])
    else:
        ax1.plot(lx, ly, label="Bola", marker = 'o', markevery=[0])
    ax1.annotate('Bola (Inicial)', (lx[0], ly[0] - 0.3), color = 'C0', ha="center")
    ax1.plot(rx, ry, marker = '.', color = 'red', label="Robô")
    ax1.annotate('Robô (Inicial)', (rx[0] + 0.3, ry[0]), color = 'red')
    ax1.annotate(("Interceptação (t = %.2f)" % tempo), (rx[1] + 0.3, ry[1] - 0.1), color = 'red')
    ax1.plot([0, 0, 9, 9, 0], [0, 6, 6, 0, 0], color = 'green', label="Campo")
    ax1.plot(rix[1], riy[1], color = 'C0', marker='.')
    ax1.plot(rix, riy, color = 'yellow', label="Raio de Intercep.")
    ax1.set(title = "Trajetória de interceptação do robô e da bola no campo", xlabel = "x (m)", ylabel = "y (m)")
    ax1.minorticks_on()
    ax1.legend()
    ax1.grid(which='both')
    ax1.grid(which='minor', alpha=0.2)
    ax1.grid(which='major', alpha=0.5)
    plt.tight_layout()
    plt.savefig("results/trajetoria_de_interceptacao.png", dpi=200)
    plt.clf()

    # Plota a trajetória x da bola e do robô pelo tempo
    fig, ax2 = plt.subplots()
    ax2.plot(lt, lx, label="Bola")
    if wait == 0:
        ax2.plot([lt[0], tempo], rx, marker = 'o', color = 'red', label="Robô")
    else:
        ax2.plot([lt[0], tempo_chegada], rx, marker = 'o', color = 'red', label="Robô")
        ax2.plot(tempo, rx[1], marker = 'o', color = 'red')
    ax2.text(tempo + 0.5, rx[1] - 0.1, ("Interceptação (t = %.2f)" % tempo), fontsize=10, color="red")
    ax2.set(title = "Posição x da bola e do robô em função do tempo", xlabel = "t (s)", ylabel = "x (m)")
    ax2.minorticks_on()
    ax2.legend()
    ax2.grid(which='both')
    ax2.grid(which='minor', alpha=0.2)
    ax2.grid(which='major', alpha=0.5)
    plt.tight_layout()
    plt.savefig("results/posicao_x_tempo.png", dpi=200)
    plt.clf()

    # Plota a trajetória y da bola e do robô pelo tempo
    fig, ax3 = plt.subplots()
    ax3.plot(lt, ly, label="Bola")
    if wait == 0:
        ax3.plot([lt[0], tempo], ry, marker = 'o', color = 'red', label="Robô")
    else:
        ax3.plot([lt[0], tempo_chegada], ry, marker = 'o', color = 'red', label="Robô")
        ax3.plot(tempo, ry[1], marker = 'o', color = 'red')
    ax3.text(tempo + 0.5, ry[1] - 0.1, ("Interceptação (t = %.2f)" % tempo), fontsize=10, color="red")
    ax3.set(title = "Posição y da bola e do robô em função do tempo", xlabel = "t (s)", ylabel = "y (m)")
    ax3.minorticks_on()
    ax3.legend()
    ax3.grid(which='both')
    ax3.grid(which='minor', alpha=0.2)
    ax3.grid(which='major', alpha=0.5)
    plt.tight_layout()
    plt.savefig("results/posicao_y_tempo.png", dpi=200)
    plt.clf()

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
    plt.clf()

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
    plt.clf()

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
    plt.clf()

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
    plt.clf()

# configura a aparencia da janela
set_appearance_mode("light")  # Modes: system (default), light, dark
set_default_color_theme("green") # Themes: blue (default), dark-blue, green

# lista as trajetorias disponiveis
trajetorias = os.listdir('trajetorias/')
files = []
for x in trajetorias:
    files.append(x[:-4])

# cria janela
window = CTk()
window.title("Projeto Ora Bolas")
window.geometry("11280x960")

frame1 = CTkFrame(window)
frame2 = CTkFrame(window, border_color="black", border_width=5, corner_radius=10)
#frame2 = Frame(window)

# cria label de seleção de trajetoria
label_trajetoria = CTkLabel(frame1, text="Selecione a trajetória desejada:", anchor="center")
label_trajetoria.pack(anchor=W, padx=10, pady=0)

# cria o menu de seleção de trajetoria
menu_trajetoria = CTkOptionMenu(master=frame1, values=files, height=40, width=200)
menu_trajetoria.pack(anchor=W, padx=10, pady=10)
menu_trajetoria.set(files[0])

# cria Frame para as entrys
inputs = CTkFrame(frame1)
inputs.pack(anchor=W, padx=10, pady=10)

# cria os inputs de posição inicial
label_posicao_inicial = CTkLabel(master=inputs, text="Posição inicial do robô (m):")
label_posicao_inicial.pack(side=TOP, padx=10, pady=10)
label_posicao_inicial_x = CTkLabel(master=inputs, text="X = ", width=20)
label_posicao_inicial_x.pack(side=LEFT, padx=5, pady=10)
input_posicao_inicial_x = CTkEntry(master=inputs, width=50)
input_posicao_inicial_x.pack(side=LEFT, padx=10, pady=10)
label_posicao_inicial_y = CTkLabel(master=inputs, text="Y = ", width=20)
label_posicao_inicial_y.pack(side=LEFT, padx=5, pady=10)
input_posicao_inicial_y = CTkEntry(master=inputs, width=50)
input_posicao_inicial_y.pack(side=LEFT, padx=10, pady=10)

# cria a função que coleta os inputs e roda o programa
def run():
    # coleta os inputs
    sx = float(input_posicao_inicial_x.get())
    sy = float(input_posicao_inicial_y.get())
    trajetoria_selecionada = menu_trajetoria.get()

    # roda o programa
    interceptacao(sx, sy, trajetoria_selecionada)

    valor = menu_grafico.get()
    exibe_imagem(valor)

    frame2.pack(side=RIGHT, padx=10, pady=10, expand=True)
    
# cria botão de execução
calcular = CTkButton(master=frame1, text="Calcular", command=run, height=40, width=200)
calcular.pack(anchor=W, padx=10, pady=10)

# cria a barra de progresso
progress_var = DoubleVar()
progress_bar = CTkProgressBar(master=frame1, orient="horizontal", mode='determinate', height=30, width=200, variable=progress_var)
progress_bar.pack(anchor=W, padx=10, pady=10)

def exibe_imagem(value):
    canvas.delete("all")

    if value == "Trajetória de interceptação":
        img_trajetoria = ImageTk.PhotoImage(Image.open("results/trajetoria_de_interceptacao.png"))
        canvas.create_image(0, 0, anchor=NW, image=img_trajetoria)
        canvas.img = img_trajetoria
    elif value == "Posição X por tempo":
        img_posicao_x_tempo = ImageTk.PhotoImage(Image.open("results/posicao_x_tempo.png"))
        canvas.create_image(0, 0, anchor=NW, image=img_posicao_x_tempo)
        canvas.img = img_posicao_x_tempo
    elif value == "Posição Y por tempo":
        img_posicao_y_tempo = ImageTk.PhotoImage(Image.open("results/posicao_y_tempo.png"))
        canvas.create_image(0, 0, anchor=NW, image=img_posicao_y_tempo)
        canvas.img = img_posicao_y_tempo
    elif value == "Velocidade X por tempo":
        img_velocidade_x_tempo = ImageTk.PhotoImage(Image.open("results/velocidade_x_tempo.png"))
        canvas.create_image(0, 0, anchor=NW, image=img_velocidade_x_tempo)
        canvas.img = img_velocidade_x_tempo
    elif value == "Velocidade Y por tempo":
        img_velocidade_y_tempo = ImageTk.PhotoImage(Image.open("results/velocidade_y_tempo.png"))
        canvas.create_image(0, 0, anchor=NW, image=img_velocidade_y_tempo)
        canvas.img = img_velocidade_y_tempo
    elif value == "Aceleração X por tempo":
        img_aceleracao_x_tempo = ImageTk.PhotoImage(Image.open("results/aceleracao_x_tempo.png"))
        canvas.create_image(0, 0, anchor=NW, image=img_aceleracao_x_tempo)
        canvas.img = img_aceleracao_x_tempo
    elif value == "Aceleração Y por tempo":
        img_aceleracao_y_tempo = ImageTk.PhotoImage(Image.open("results/aceleracao_y_tempo.png"))
        canvas.create_image(0, 0, anchor=NW, image=img_aceleracao_y_tempo)
        canvas.img = img_aceleracao_y_tempo

    window.update()

# cria label menu gráfico
label_graficos = CTkLabel(frame1, text="Selecione o gráfico desejado:", anchor="center")
label_graficos.pack(anchor=W, padx=10, pady=0)

# cria o menu de seleção de gráfico
menu_grafico = CTkOptionMenu(master=frame1, values=["Trajetória de interceptação", "Posição X por tempo", "Posição Y por tempo", "Velocidade X por tempo", "Velocidade Y por tempo", "Aceleração X por tempo", "Aceleração Y por tempo"], height=40, width=200, command=exibe_imagem)
menu_grafico.pack(anchor=W, padx=10, pady=10)
menu_grafico.set("Trajetória de interceptação")

canvas = Canvas(frame2, width=1280, height=960)
canvas.pack(anchor=CENTER, padx=10, pady=10)

def update_progress(value):
    progress_var.set(value)
    window.update()

frame1.pack(side=LEFT, padx=10, pady=10)


# mainloop
window.mainloop()
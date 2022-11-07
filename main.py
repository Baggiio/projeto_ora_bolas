from math import *
import os, subprocess, sys
from zoom_advanced import Zoom_Advanced
from time import sleep

try:
    import numpy as np
except ImportError or ModuleNotFoundError:
    print("Numpy não instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError or ModuleNotFoundError:
    print("Matplotlib não instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt

try:
    from tkinter import *
except ImportError or ModuleNotFoundError:
    print("Tkinter não instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinter"])
    from tkinter import *

try:
    from customtkinter import *
except ImportError or ModuleNotFoundError:
    print("Customtkinter não instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    from customtkinter import *

try:
    from PIL import ImageTk, Image
except ImportError or ModuleNotFoundError:
    print("PIL não instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import ImageTk, Image

def interceptacao(sx, sy, arquivo):

    # Incializa as listas vazias para armazenar os valores de t, x e y
    global lx, ly
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

    # Aproxima uma função polinomial para a trajetória da bola
    fx = np.polyfit(lt, lx, 3).tolist()
    fy = np.polyfit(lt, ly, 2).tolist()

    # Deriva a posição para obter a velocidade
    fdx = np.polyder(fx).tolist()
    fdy = np.polyder(fy).tolist()

    # Deriva a velocidade para obter a aceleração
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

    # Cria a lista de distãncias entre a bola e o robô
    dist = []
    t_dist = []
    for i in range(len(lt)):
        if wait == 1 and lt[i] >= tempo_chegada:
            rx_all = lx[waitj+2]
            ry_all = ly[waitj+2]
        else:
            rx_all = sx + vxf*lt[i]
            ry_all = sy + vyf*lt[i]
        dist.append(sqrt((lx[i]-rx_all)**2 + (ly[i]-ry_all)**2))
        t_dist.append(lt[i])
        if lt[i] >= tempo:
            break

    global rx_return, ry_return, t_return

    rx_return = []
    ry_return = []
    t_return = []
    for i in range(len(lt)):
        if wait == 1 and lt[i] > tempo_chegada:
            break
        t_return.append(lt[i])
        rx_return.append(sx + vxf*lt[i])
        ry_return.append(sy + vyf*lt[i])
        if lt[i] >= tempo:
            break

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
    ax2.text(tempo + 0.5, rx[1] - 0.1, ("Interceptação (t = %.2f s)" % tempo), fontsize=10, color="red")
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
    ax3.text(tempo + 0.5, ry[1] - 0.1, ("Interceptação (t = %.2f s)" % tempo), fontsize=10, color="red")
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
    ax4.plot(lt, vbx, label="Bola", marker='o', markevery=[0, -1])
    ax4.plot([lt[0], lt[-1]], [vxf, vxf], color = 'red', label="Robô", marker='o', markevery=[0, -1])
    ax4.annotate(('%.2f m/s' % vxf), (lt[0] + 0.5, vxf + 0.2), color = 'red')
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
    ax5.plot(lt, vby, label="Bola", marker='o', markevery=[0, -1])
    ax5.plot([lt[0], lt[-1]], [vyf, vyf], color = 'red', label="Robô", marker='o', markevery=[0, -1])
    ax5.annotate(('%.2f m/s' % vyf), (lt[0] + 0.5, vyf + 0.2), color = 'red')
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
    ax6.plot(lt, abx, label="Bola", marker='o', markevery=[0, -1])
    ax6.plot([lt[0], lt[-1]], [0, 0], color = 'red', label="Robô", marker='o', markevery=[0, -1])
    ax6.annotate(("%.2f m/s²" % 0), (lt[0], 0.002), color = 'red')
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
    ax7.plot(lt, aby, label="Bola", marker='o', markevery=[0, -1])
    ax7.plot([lt[0], lt[-1]], [0, 0], color = 'red', label="Robô", marker='o', markevery=[0, -1])
    ax7.annotate(("%.2f m/s²" % 0), (lt[0], 0.002), color = 'red')
    ax7.set(title = "Aceleração y da bola e do robô em função do tempo", xlabel = "t (s)", ylabel = "Ay (m/s²)")
    ax7.minorticks_on()
    ax7.legend()
    ax7.grid(which='both')
    ax7.grid(which='minor', alpha=0.2)
    ax7.grid(which='major', alpha=0.5)
    plt.tight_layout()
    plt.savefig("results/aceleracao_y_tempo.png", dpi=200)
    plt.clf()

    # Plota a distancia relativa entre bola e robô
    fig, ax8 = plt.subplots()
    ax8.plot(t_dist, dist, label="Distancia Relativa", marker='o', markevery=[0, -1])
    ax8.annotate(("%.4f m" % 0.0965), xy=(t_dist[dist.index(min(dist))], min(dist)), xytext=(t_dist[dist.index(min(dist))], min(dist) + 0.1), color = "C0")
    ax8.set(title = "Distância relativa entre robô e bola em função do tempo", xlabel = "t (s)", ylabel = "d (m)")
    ax8.minorticks_on()
    ax8.grid(which='both')
    ax8.grid(which='minor', alpha=0.2)
    ax8.grid(which='major', alpha=0.5)
    plt.tight_layout()
    plt.savefig("results/distancia_relativa.png", dpi=200)
    plt.clf()

    # Exibe os resultados
    label_results.configure(text="Ponto de interceptação no menor tempo encontrado!")
    if wait == 1:
        label_wait.configure(text=("O robô chegará no instante t = %.2f s e deverá\nesperar a bola retornar ao campo." % tempo_chegada))
    else:
        label_wait.configure(text='')
    label_intercept.configure(text=("O robô interceptará a bola no instante t = %.2f s." % tempo))
    label_velocidade.configure(text=("Para isso, o robô deve utilizar uma velocidade de Vx = %.2f e Vy = %.2f." % (vxf, vyf)))


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
window.state("zoomed")

# cria os frames (divisoes) do programa
frame1 = CTkFrame(window)
frame2 = CTkFrame(window, border_color="black", border_width=5, corner_radius=10)
frame3 = CTkFrame(window, border_color="black", border_width=5, corner_radius=10)

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

    # cria o campo
    canvas_campo.delete("all")
    canvas_campo.create_image(0, 0, image=img_campo, anchor=NW)
    canvas_campo.img = img_campo

    # cria o robo
    canvas_campo.create_image(sx*142.23, 853-(sy*142.17), anchor=NW, image=img_robo)
    canvas_campo.img = img_robo

    # cria a bola
    canvas_campo.create_image(lx[0]*142.23, 853-(ly[0]*142.17), anchor=NW, image=img_bola)
    canvas_campo.imgbola = img_bola
    
# cria botão de execução
calcular = CTkButton(master=frame1, text="Calcular", command=run, height=40, width=200)
calcular.pack(anchor=W, padx=10, pady=10)

# cria a barra de progresso
progress_var = DoubleVar()
progress_bar = CTkProgressBar(master=frame1, orient="horizontal", mode='determinate', height=30, width=200, variable=progress_var)
progress_bar.pack(anchor=W, padx=10, pady=10)

# exibe imagem com zoom:
def exibe_imagem(value):
    canvas.delete("all")
    frame3.pack_forget()
    frame2.pack(side=RIGHT, padx=10, pady=10, expand=True)

    if value == "Trajetória de interceptação":
        Zoom_Advanced(canvas, path="results/trajetoria_de_interceptacao.png")
    elif value == "Posição X por tempo":
        Zoom_Advanced(canvas, path="results/posicao_x_tempo.png")
    elif value == "Posição Y por tempo":
        Zoom_Advanced(canvas, path="results/posicao_y_tempo.png")
    elif value == "Velocidade X por tempo":
        Zoom_Advanced(canvas, path="results/velocidade_x_tempo.png")
    elif value == "Velocidade Y por tempo":
        Zoom_Advanced(canvas, path="results/velocidade_y_tempo.png")
    elif value == "Aceleração X por tempo":
        Zoom_Advanced(canvas, path="results/aceleracao_x_tempo.png")
    elif value == "Aceleração Y por tempo":
        Zoom_Advanced(canvas, path="results/aceleracao_y_tempo.png")
    elif value == "Distância Relativa":
        Zoom_Advanced(canvas, path="results/distancia_relativa.png")
    elif value == "Simulação":
        frame2.pack_forget()
        frame3.pack(side=RIGHT, padx=10, pady=10, expand=True)

    window.update()

# cria label menu gráfico
label_graficos = CTkLabel(frame1, text="Selecione a saída desejada:", anchor="center")
label_graficos.pack(anchor=W, padx=10, pady=0)

# cria o menu de seleção de gráfico
menu_grafico = CTkOptionMenu(master=frame1, values=["Trajetória de interceptação", "Posição X por tempo", "Posição Y por tempo", "Velocidade X por tempo", "Velocidade Y por tempo", "Aceleração X por tempo", "Aceleração Y por tempo", "Distância Relativa", "Simulação"], height=40, width=200, command=exibe_imagem)
menu_grafico.pack(anchor=W, padx=10, pady=10)
menu_grafico.set("Trajetória de interceptação")

# cria o canvas para exibir as imagens
canvas = Canvas(frame2, width=1280, height=960)
canvas.pack(anchor=CENTER, padx=10, pady=10)

# cria o canvas do campo
canvas_campo = Canvas(frame3, width=1280, height=853)
canvas_campo.pack(anchor=SE, padx=10, pady=10)

# abre a imagem da bola e do robo
img_bola = ImageTk.PhotoImage(Image.open("images/ball.png"))

# abre a imagem do campo
img_campo = ImageTk.PhotoImage(Image.open("images/campo.png"))
img_robo = ImageTk.PhotoImage(Image.open("images/robot.png").rotate(180))

# exibe a imagem do campo no canvas_campo
canvas_campo.create_image(0, 0, anchor=SW, image=img_campo)
canvas_campo.img = img_campo

def iniciar_simulacao():
    tg = (lx[len(t_return)]-rx_return[0])/(ly[len(t_return)]-ry_return[0])
    ang = atan(tg)
    ang = degrees(ang)
    if rx_return[0] > lx[len(t_return)] and ry_return[0] < ly[len(t_return)]:
        ang = -ang
    elif rx_return[0] > lx[len(t_return)] and ry_return[0] > ly[len(t_return)]:
        ang = ang + 90
    else:
        ang = ang - 90
    img_robo = ImageTk.PhotoImage(Image.open("images/robot.png").rotate(270+ang))
    canvas.test = img_robo

    for i in range(len(t_return)):
        canvas_campo.delete("all")
        canvas_campo.create_image(0, 0, anchor=NW, image=img_campo)
        canvas_campo.img = img_campo
        if i > len(t_return) - 2:
            canvas_campo.create_image(rx_return[len(t_return)-2]*142.23, 853-(ry_return[len(t_return)-2]*142.17), anchor=CENTER, image=img_robo)
        else:
            canvas_campo.create_image(rx_return[i]*142.23, 853-(ry_return[i]*142.17), anchor=CENTER, image=img_robo)
        canvas_campo.create_image(lx[i]*142.23, 853-(ly[i]*142.17), anchor=CENTER, image=img_bola)
        canvas_campo.update()
        sleep(0.02)

    sleep(3)

    # cria o campo
    canvas_campo.delete("all")
    canvas_campo.create_image(0, 0, image=img_campo, anchor=NW)
    canvas_campo.img = img_campo

    # cria o robo
    canvas_campo.create_image(rx_return[0]*142.23, 853-(ry_return[0]*142.17), anchor=NW, image=img_robo)
    canvas_campo.img = img_robo

    # cria a bola
    canvas_campo.create_image(lx[0]*142.23, 853-(ly[0]*142.17), anchor=NW, image=img_bola)
    canvas_campo.imgbola = img_bola

# cria o botão para iniciar a simulação
button_iniciar = CTkButton(frame3, text="Iniciar", command=iniciar_simulacao)
button_iniciar.pack(anchor=CENTER, padx=10, pady=10)

# cria os labels de resultado
label_results = CTkLabel(frame1, text='')
label_results.pack(anchor=W, padx=10, pady=1)
label_intercept = CTkLabel(frame1, text='')
label_intercept.pack(anchor=W, padx=10, pady=1)
label_velocidade = CTkLabel(frame1, text='')
label_velocidade.pack(anchor=W, padx=10, pady=1)
label_wait = CTkLabel(frame1, text='')
label_wait.pack(anchor=W, padx=10, pady=1)

# cria a função que atualiza a barra de progresso
def update_progress(value):
    progress_var.set(value)
    window.update()

# exibe o menu lateral
frame1.pack(side=LEFT, padx=10, pady=10)

# mainloop
window.mainloop()
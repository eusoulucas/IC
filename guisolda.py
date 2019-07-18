import serial  # Comunicação
import matplotlib.pyplot as plt
from tkinter import *  # Biblioteca para fazer interface
from PIL import Image, ImageTk  # Biblioteca para uso de imagens

global counter
counter = 0


def criar_porta():
    global portaUSB
    aux = temp.get()
    str(aux)
    portaUSB = serial.Serial(aux, 500000)


def defi_tempo():
    global vari
    vari = var.get()

def click():
    j = 0
    #dados = open("dados.txt", "wb")
    while j < vari:
        info = portaUSB.read(4)
        #dados.write(info)
        j = j + 1

    #dados.close()

    t = []
    corrente = []
    tensao = []


    dados = open("dados.txt", "r")

    for line in dados:
        line = line.strip("ÿ")
        line = line.strip()
        Y,Z,X = line.split(",")
        t.append(X)
        corrente.append(Y)
        tensao.append(Z)

    dados.close()

    # usuario define o tempo de aquisição
    # velocidade de aquisição em defaut
    # plotar dados salvos diretos do arduino
    # eliminar comunicação serial para ganhar em velocidade
    # graficos na janela principal
    # eliminar start

    plt.plot(t, tensao, label="Tensão")
    plt.plot(t, corrente, label="Corrente")
    plt.title("Tensão/Corrente X Tempo")
    plt.xlabel("Tempo")
    plt.ylabel("Corrente/Tensão")
    plt.legend()
    plt.savefig("Grafico_val.png", dpi=60)
    image_val = ImageTk.PhotoImage(file='Grafico_val.png')
    label_val = Label(janela, image=image_val)
    label_val.place(x=60, y=190)


def sair():
    janela.destroy()


janela = Tk()

janela.title('LEITURA DE DADOS')
janela.geometry("500x500")
janela.configure(bg='lightblue')

image0 = ImageTk.PhotoImage(file='ufu.png')
label_0 = Label(janela, image=image0, bg='white')
label_0.pack()

image_val = ImageTk.PhotoImage(file='Grafico_val.png')
label_val = Label(janela, image=image_val)
label_val.place(x=60, y=190)

texto_porta = Label(text="Informe a porta", bg='darkblue', fg='white').place(x=80, y=20)
temp = StringVar()
porta = Entry(janela, textvariable=temp, bg='white').place(x=170, y=20)
bot_porta = Button(text="OK", command=criar_porta, bg='darkblue', fg='white').place(x=300, y=20)

texto_tempo = Label(text="Informe a tempo de aquisição", bg='darkblue', fg='white').place(x=5, y=60)
var = IntVar()
tempo = Entry(janela, textvariable=var, bg='white').place(x=170, y=60)
bot_tempo = Button(text="OK", command=defi_tempo, bg='darkblue', fg='white').place(x=300, y=60)

bt_val = Button(janela, width=20, text='START', command = click, bg='green', fg='white')
bt_val.place(x=170, y=100)

bt_exit = Button(janela, width=20, text='SAIR', command=sair, bg='red', fg='white')
bt_exit.place(x=170, y=150)

janela.mainloop()

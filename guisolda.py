import serial #Comunicação
import matplotlib.pyplot as plt
from tkinter import *  # Biblioteca para fazer interface
from PIL import Image, ImageTk  #Biblioteca para uso de imagens

import threading
import time

global counter
counter = 0

def criar_porta():
    global portaUSB
    aux = temp.get()
    str(aux)
    portaUSB = serial.Serial(aux, 500000)

def def_tempo():
    var = var.get()
    str(var)
    portaUSB.write(var.encode())

def click(janela2):
    dados = portaUSB.read(8)
    corrente = Label(janela2, text = dados[0:4], fg  = 'blue', bg = 'lightblue')
    corrente.place(x = 100, y = 40)
    tensao = Label(janela2, text = dados[4:], fg  = 'blue', bg = 'lightblue')
    tensao.place(x = 100, y = 70)
    text = str(dados)
    dados.write(text)
    if counter < 1:
        janela2.after(1, lambda: click(janela2))

def jan_read():
    janela2 = Tk()
    janela2.title('Valores')
    janela2.geometry("220x140")
    janela2.configure(bg = 'lightblue')

    texto_A = Label(janela2, text='CORRENTE:', bg = 'blue')
    texto_A.place(x = 10, y = 40)
    texto_V = Label(janela2, text='TENSÃO:', bg = 'blue')
    texto_V.place(x = 10, y = 70)

    grandeza_A = Label(janela2, text='[A]', bg = 'blue')
    grandeza_A.place(x= 130, y = 70)
    grandeza_V = Label(janela2, text='[V]', bg = 'blue')
    grandeza_V.place(x= 130, y = 40)
    click(janela2)

def sair():
    janela.destroy()

janela = Tk()

janela.title('LEITURA DE DADOS')
janela.geometry("500x500")
janela.configure(bg = 'lightblue')

t = []
corrente = []
tensao = []

dados = open("dados.txt", "r")

for line in dados:
    line = line.strip()
    Y,X,Z = line.split(",")
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

plt.plot(t, tensao, label = "Tensão")
plt.plot(t, corrente, label = "Corrente")
plt.title("Tensão/Corrente X Tempo")
plt.xlabel("Tempo")
plt.ylabel("Corrente/Tensão")
plt.legend()
plt.savefig("Grafico_val.png", dpi = 60)

image0 = ImageTk.PhotoImage(file = 'ufu.png')
label_0 = Label(janela, image = image0, bg = 'white')
label_0.pack()

image_val = ImageTk.PhotoImage(file='Grafico_val.png')
label_val = Label(janela, image = image_val)
label_val.place(x= 60, y = 190)

texto_porta = Label(text = "Informe a porta", bg = 'darkblue', fg = 'white').place(x = 80, y = 20)
temp = StringVar()
porta = Entry(janela, textvariable = temp, bg = 'white').place(x = 170, y = 20)
bot_porta = Button(text = "OK", command = criar_porta, bg = 'darkblue', fg = 'white').place(x = 300, y = 20)

texto_tempo = Label(text = "Informe a tempo de aquisição", bg = 'darkblue',fg = 'white').place(x = 5, y = 60)
var = StringVar()
tempo = Entry(janela, textvariable = var, bg = 'white').place(x = 170, y = 60)
bot_tempo = Button(text = "OK", command = def_tempo, bg = 'darkblue', fg = 'white').place(x = 300, y = 60)

bt_val = Button(janela, width = 20, text = 'START', command = jan_read, bg = 'green', fg = 'white')
bt_val.place(x = 170, y = 100)

bt_exit = Button(janela, width = 20, text = 'SAIR', command = sair, bg = 'red', fg = 'white')
bt_exit.place(x = 170, y = 150)

janela.mainloop()

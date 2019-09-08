import serial  # Comunicação
import matplotlib.pyplot as plt
from tkinter import *  # Biblioteca para fazer interface
from PIL import Image, ImageTk  # Biblioteca para uso de imagens
import time

global counter
counter = 0

def criar_porta():
    global portaUSB
    aux = temp.get()

    str(aux)
    try:
        portaUSB = serial.Serial(aux, 500000)
    except:
        l_status = Label(status, text="Porta invalida!                   ", fg="red",bg="#FFFFFF" )
        l_status.place(relx="0.3", rely="0.01")
    else:
        l_status = Label(status, text="Digite o tempo de aquisição        ", fg="black",bg="#FFFFFF" )
        l_status.place(relx="0.3", rely="0.01")

def defi_tempo():
    global vari
    try:
        vari = var.get()
        #ATE AQUI O PROGRAMA TÁ UMA BELEUZURA
    except:
        l_status = Label(status, text="Um erro ocorreu                 ",
                         fg="red",bg="#FFFFFF" )
        l_status.place(relx="0.3", rely="0.01")
    else:
        l_status = Label(status, text="Clique START para iniciar a aquisição",
                         fg="green",bg="#FFFFFF" )
        l_status.place(relx="0.3", rely="0.01")
        
    

def click():
    try:
        data = portaUSB.readline(end = "")
    except:
        l_status = Label(status, text="Um erro ocorreu                                         ",
                         bg="#FFFFFF" ,  fg="red")
        l_status.place(relx="0.3", rely="0.01")
    else:
        info = str(data)
        Y, Z, X = info.split(",")
        print(int(X))
        lim = int(X) + vari

        dados = open("dados.txt", "wb")
        while int(X) < lim:
            data = portaUSB.readline()
            info = str(data)
            Y, Z, X = info.split(",")
            dados.write(info[:2])

        dados.close()

        t = []
        corrente = []
        tensao = []

        dados = open("dados.txt", "r")

        for line in dados:
            Y,Z,X = line.split(",")
            t.append(X)
            corrente.append(Y)
            tensao.append(Z)

        dados.close()

        # plotar dados salvos diretos do arduino
        # eliminar comunicação serial para ganhar em velocidade

        plt.plot(t, tensao, label = "Tensão")
        plt.plot(t, corrente, label = "Corrente")
        plt.title("Tensão/Corrente X Tempo")
        plt.xlabel("Tempo")
        plt.ylabel("Corrente/Tensão")
        plt.legend(loc = 5)
        plt.legend()
        plt.savefig("Grafico_val.png", dpi=60)
        plt.close()
        image_val = ImageTk.PhotoImage(file='Grafico_val.png')
        label_val = Label(janela, image=image_val)
        label_val.place(x=60, y=190)

        janela.mainloop()

def sair():
    janela.destroy()

janela = Tk()

janela.title('LEITURA DE DADOS')
janela.geometry("500x500")

image0 = ImageTk.PhotoImage(file='back.jpg')
label_0 = Label(janela, image=image0, bg='white')
label_0.place(x=0, y=0, relwidth=1, relheight=1)

frame3 = Frame(janela, bg = "#00FFFF", highlightthickness=0)
frame3.place(relx="0.12", rely="0.35", relwidth="0.77", relheight= "0.58")

image_val = PhotoImage(file='Grafico_val.png')
label_val = Label(frame3, image=image_val)
label_val.place(relwidth="1.0", relheight="1.0")

frame1 = Frame(janela, bg = "#4169E1", bd=3, highlightthickness=0)
frame1.place(relx="0.10", rely="0.05", relwidth="0.8", relheight="0.13")

frame2 = Frame(janela, bg = "#00FFFF")
frame2.place(relx="0.32", rely="0.22", relwidth="0.34", relheight="0.1059999")

status = Frame(janela, bg="white")
status.place(relx="0.10", rely="0.94", relwidth="0.8", relheight="0.05")

l_status = Label(status, text="Selecione uma porta USB", fg="black",bg="#FFFFFF" )
l_status.place(relx="0.3", rely="0.01")

texto_porta = Label(frame1,text="PORTA", bg="#4169E1",
                    fg='white', font="Britannic 10")
texto_porta.place(relx="0", rely="0")
temp = StringVar()
porta = Entry(frame1, textvariable=temp, bg='white', font="Britannic 12", bd="0")
porta.place(relx="0.44", rely="0.02")
bot_porta = Button(frame1, text="OK", command=criar_porta, bg='darkblue', 
                    fg='white', font="Britannic 10", bd= 0)
bot_porta.place(relx="0.921", rely="0.02")

texto_tempo = Label(frame1, text="TEMPO DE AQUISIÇÃO", bg="#4169E1", 
                    fg='white', font="Britannic 10")
texto_tempo.place(relx="0", rely="0.5")
var = IntVar()
tempo = Entry(frame1, textvariable=var, bg='white', font="Britannic 12", bd="0")
tempo.place(relx="0.44", rely="0.5")
bot_tempo = Button(frame1, text="OK", command=defi_tempo, bg='darkblue', 
                    fg='white', font="Britannic 10", bd= 0)
bot_tempo.place(relx="0.921", rely="0.5")

bt_val = Button(frame2, width=20, text='START', command = click, bg='green', 
                fg='white', bd=0, font="Britannic 10")
bt_val.place(relx="0.01", rely="0.045", relwidth="0.97", relheight= "0.40")

bt_exit = Button(frame2, width=20, text='SAIR', command=sair, bg='red', 
                fg='white', bd=0, font="Britannic 10")
bt_exit.place(relx="0.01", rely="0.53", relwidth="0.97", relheight= "0.40")

janela.mainloop()

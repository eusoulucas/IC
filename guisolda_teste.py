import serial  # Comunicação
import matplotlib.pyplot as plt # plotar graficos
from tkinter import *  # Biblioteca para fazer interface
from PIL import Image, ImageTk  # Biblioteca para uso de imagens
from datetime import datetime # data e hora 
import time # funçao sleep e process_time()

def criar_porta():
    global portaUSB  #definindo variavel global
    aux = temp.get()  #"pega" oque esta escrito na variavel temp
    str(aux)
    try:
        portaUSB = serial.Serial(aux, 500000) #tentado estabelecer comunicação com o arduino
    except: #caso a comunicacao falhe por algum motivo
        status_erro = Label(status_error, text="Um erro ocorreu",
                        fg="red",bg="#FFFFFF", font="Britannic 13") #preenchendo o label com mens de erro
        status_erro.place(relx="0.3", rely="0.01", relheight="0.9")  
    else: #caso haja sucesso na comunicação
        status_tme = Frame(janela, bg="white") #criando frame para aquisição do tempo de aquisição
        status_tme.place(relx="0.10", rely="0.94", relwidth="0.8", relheight="0.05")
        status_time = Label(status_tme, text="Digite o tempo de aquisição", 
                        fg="black",bg="#FFFFFF", font="Britannic 13")
        status_time.place(relx="0.3", rely="0.01", relheight="0.9")

def defi_tempo():
    global vari #definido variavel global
    try:
        vari = var.get() #"pegando" valor salvo em var
    except: #caso haja um valor possivel var
        status_erro = Label(status_error, text="Um erro ocorreu",font="Britannic 13",
                        fg="red",bg="#FFFFFF") #preenchendo barra com mens de erro
        status_erro.place(relx="0.3", rely="0.01", relheight="0.9")
    else:
        status_plot = Label(status_0, text="Clique PLOTAR para plotar o gráfico",font="Britannic 13",
                        fg="green",bg="#FFFFFF" ) #exibindo mensagem seguinte
        status_plot.place(relx="0.15", rely="0.01", relheight="0.9")
        
def plot():
    try:
        data = str(datetime.now()) #atribuindo data e hora à data
        file_name = "data_files/Dados"+ data #criando nome do arquivo
        #as tres linha subsequentes são modificações para que os arquivos sejam passiveis de serem salvos
        file_name = file_name.replace(":","-")
        file_name = file_name.replace(".","-")
        file_name = file_name.replace(" ","-") 
        file_name = file_name + ".txt" #adicionando a extensão
        dados = open(file_name, "w") #abrindo arquivo em modo de escrita
        
        while time.process_time() < vari:
            data = portaUSB.readline() #lendo informações da porta serial
            info = str(data) # convertendo para string
            #as tres linha subsequentes são modificações para que os dados sejam passiveis de serem plotados
            info = info.replace("\\xff","") 
            info = info.replace("\\r", "")
            info = info.replace("\\n","")
            info = info.replace("'","")
            info = info.replace("b","")
            dados.write(info)  #escrevendo dados no arquivo
            dados.write("\n") #pulando linha
            Y, Z, X = info.split(",") #definido vetores de dados
            i = int(X)/1000
        dados.close() #fechando arquivos
    except:
        status_error.place(relx="0.10", rely="0.94", relwidth="0.8", relheight="0.05")
        status_erro = Label(status_error, text="Um erro ocorreu",font="Britannic 13",
                        fg="red",bg="#FFFFFF" )
        status_erro.place(relx="0.3", rely="0.01", relheight="0.9")
    else:
        #definindo vetores
        t = []
        corrente = []
        tensao = []

        dados = open(file_name, "r") #abrindo arquivos em modo de leitura

        for line in dados: #laço para preencher vetores
            Y,Z,X = line.split(",")
            t.append(X)
            corrente.append(Y)
            tensao.append(Z)

        dados.close() #fechando arquivo

        data = str(datetime.now()) #atribuindo data e hora à data
        img_name = "graphs/grafico" + data #definindo nome do arquivos
        #as tres linha subsequentes são modificações para que os arquivos sejam passiveis de serem salvos
        img_name = img_name.replace(":","-")
        img_name = img_name.replace(".","-")
        img_name = img_name.replace(" ","-") 
        img_name = img_name + ".png" #definindo extensão do arq

        plt.axis((0,5,0,5))
        plt.plot(t, tensao, label = "Tensão") #plotando grafico TEMPOxTENSÃO
        plt.plot(t, corrente, label = "Corrente") #plotando grafico TEMPOxCORRENTE
        plt.title("Tensão/Corrente X Tempo")
        plt.xlabel("Tempo")
        plt.ylabel("Corrente/Tensão")
        plt.legend(loc = 5)
        plt.legend()
        plt.savefig(img_name, dpi=60)
        plt.close()
        image_val = ImageTk.PhotoImage(file=img_name)
        label_val = Label(frame3, image=image_val)
        label_val.place(relwidth="1.0", relheight="1.0")

        janela.mainloop()

def sair():
    janela.destroy()

janela = Tk()  #criando janela

janela.title('LEITURA DE DADOS') # definindo atributo titulo da janela
janela.geometry("500x500") # definindo tamanho inicial da janlea

image0 = ImageTk.PhotoImage(file='images/back.jpg') #criando objeto de imagem
label_0 = Label(janela, image=image0, bg='white') #atribuindo imagem a janela
label_0.place(x=0, y=0, relwidth=1, relheight=1) #definioes espaciais da janela

frame3 = Frame(janela, bg = "#00FFFF", highlightthickness=0) #criando frame para o grafico
frame3.place(relx="0.12", rely="0.35", relwidth="0.77", relheight= "0.58") #definicoes espaciais do frame

image_val = PhotoImage(file="graphs/Grafico_sample.png") #criando objeto de imagem com o grafico plotado(nesse inicio não ha grafico)
label_val = Label(frame3, image=image_val) #atribuindo grafico ao frame
label_val.place(relwidth="1.0", relheight="1.0") # definiçoes espaciais do frame

frame1 = Frame(janela, bg = "#4169E1", bd=3, highlightthickness=0) #criando frame para inputs
frame1.place(relx="0.10", rely="0.05", relwidth="0.8", relheight="0.13") #definicoes espaciais

frame2 = Frame(janela, bg = "#00FFFF") #criando frame para buttons
frame2.place(relx="0.32", rely="0.22", relwidth="0.34", relheight="0.1059999") #definicoes espaciais

status_0 = Frame(janela, bg="white") #criando frame para barra de mensagens (status do sistema)
status_0.place(relx="0.10", rely="0.94", relwidth="0.8", relheight="0.05") #definicoes espaciais
status_porta = Label(status_0, text="Selecione uma porta USB", fg="black",bg="#FFFFFF", font="Britannic 13") #preenchendo frame status
status_porta.place(relx="0.3", rely="0.01")#definicoes espaciais

status_error = Frame(janela, bg="white") #definindo frame da barra de err

texto_porta = Label(frame1,text="PORTA", bg="#4169E1",
                    fg='white', font="Britannic 10") #preenchendo frame1
texto_porta.place(relx="0", rely="0") #definicoes espaciais
temp = StringVar() #defiinindo variavel de texto temp
porta = Entry(frame1, textvariable=temp, bg='white', font="Britannic 12", bd="0") #salvando texto digitado na varaivel temp
porta.place(relx="0.44", rely="0.02") #definicoes espaciais
bot_porta = Button(frame1, text="OK", command=criar_porta, bg='darkblue', 
                    fg='white', font="Britannic 10", bd= 0) #botão que chama função de criar a porta
bot_porta.place(relx="0.921", rely="0.02") #definicoes espaciais

texto_tempo = Label(frame1, text="TEMPO DE AQUISIÇÃO", bg="#4169E1", 
                    fg='white', font="Britannic 10") #preenchendo frame1
texto_tempo.place(relx="0", rely="0.5") #definições espaciais
var = IntVar() #criando uma varaivel do tipo inteiro
tempo = Entry(frame1, textvariable=var, bg='white', font="Britannic 12", bd="0") #salvando tempo de aquisição na variavel
tempo.place(relx="0.44", rely="0.5") #definições espaciais
bot_tempo = Button(frame1, text="OK", command=defi_tempo, bg='darkblue', 
                    fg='white', font="Britannic 10", bd= 0) #botão que chama a função de definir tempo 
bot_tempo.place(relx="0.921", rely="0.5") #definições espaciais

bt_val = Button(frame2, width=20, text='PLOTAR', command = plot, bg='green', 
                fg='white', bd=0, font="Britannic 10") #botão que chama a func plota grafico
bt_val.place(relx="0.01", rely="0.045", relwidth="0.97", relheight= "0.40")

bt_exit = Button(frame2, width=20, text='SAIR', command=sair, bg='red', 
                fg='white', bd=0, font="Britannic 10") #botao que destroi a janela
bt_exit.place(relx="0.01", rely="0.53", relwidth="0.97", relheight= "0.40")

janela.mainloop() #loop eterno
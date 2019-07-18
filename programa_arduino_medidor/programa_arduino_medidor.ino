
#define amostra 16 //n° de amostras por ciclo
#include <TimerOne.h>
#include <DS1307.h>
#include <SPI.h>
#include <SD.h>

File Dados; //Definindo nome do arquivo
int VT = (1/0.303030303030)*220/2.2; // Conversão de 1 volt para VT (sensor) ??
int VC = (1/0.303030303030)*50/5/2; // Conversão de 1 volt para VC (sensor) ??

float potenciaAt = 0;

const float Const = 0.00322265625; //3.3/1023

int def = 465; // Variavel para offset da onda do sensor ??


// Arrays para gravação
float GraV1 [12]={};
float GraC1 [12]={};
float GraP1 [12]={};

float GraV2 [15]={};
float GraC2 [15]={};
float GraP2 [15]={};


//Modulo RTC DS1307 ligado as portas A4 e A5 do Arduino
DS1307 rtc(A4, A5);//SDA ~> A4; SCL ~> A5

// Zerando as variáveis condição para passar o if na rotina de gravação
byte P1 = 0;
byte P2 = 0;
byte P3 = 0;

// Definindo os ponteiros
float *ponteiroC;
float *ponteiroV;
float *ponteiroP;

byte senC = A1; //Porta sensor de corrente
byte senT = A0; //Porta sensor de tensão

// Definindo vetores
float  Pcorrente[amostra] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
float  Ptensao[amostra] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
float  Ppotencia[amostra] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

volatile byte Vex = 0; // ???

byte frequencia = 60;
long interrupcao = 1041; //((1/frequencia)/amostra)*1000000; Intervalo que a interrupção deve ser chamada, ou seja, aqui é configurado a taxa de amostragem 
// ou a freq de aquisição, este valor está me definindo uma freq de aquisação de 960 Hz. Para 10 kHz esse valor seria 100.

void setup() 
{
  Serial.begin(9600);
	analogReference(EXTERNAL); //Definir referencia de entrada com AREF(3.3v), deve ser colocado o sinal de 3.3v neste pino (AREF)
	pinMode(senT,INPUT);
	pinMode(senC,INPUT);
  pinMode(A2, OUTPUT); //alimentação do relógio
  pinMode(A3, OUTPUT);

  digitalWrite(A2, 0); //GND do relógio
  digitalWrite(A3, 1); //+5v do relógio
  
  //Aciona o relógio
  rtc.halt(false);
 
  //Definicoes do pino SQW/Out
  rtc.setSQWRate(SQW_RATE_1);
  rtc.enableSQW(true);
        
  // Inicializando SD
  if (!SD.begin(4)) {
  Serial.println("Falha na inicializancao SD");
  return;} // acredito que não teria necessidade ?!
        
  // Inicializando as configurações da interrupção
  Timer1.initialize(interrupcao); // tempor em microseg que a interrupção deve ser chamada
  Timer1.attachInterrupt(Tvetor, interrupcao); // Atribui uma função para ser chamada a cada interrupção gerada pelo timer, "interrupção" é o período 
  Serial.println(".");   
}

void loop() 
{
}

// Função do timer1
void Tvetor()
{ 
	//Armazenando valores de corrente
	for(byte x=0;x<(amostra-1);x++) // termina quando x = amostra-1
		Pcorrente[(amostra-x-1)] = Pcorrente[(amostra-x-2)];
		
	//Calculando tensão do sensor de corrente
	Pcorrente[0] = (analogRead(senC)-def)*Const*VC; // def = 465, Const = 0.00322265625 (3.3/1023), e VC = (1/0.303030303030)*50/5/2 ?????????

	//Armazenando valores de tensão
	for(byte x=0;x<(amostra-1);x++)
		Ptensao[(amostra-x-1)] = Ptensao[(amostra-x-2)];
		
	//Calculando tensão do sensor de tensão
	Ptensao[0] = (analogRead(senT)-def)*Const*VT;
 
	
	//Calculando potencia
        
  potenciaAt = 0; // Pontência Ativa ?
	for(byte x=0;x<(amostra);x++)
	 {
	  Ppotencia[x] = Pcorrente[x]*Ptensao[x]; // calculando potência instantanea 
    potenciaAt = Ppotencia[x]+potenciaAt; // somando as potências
	 } 
   
  potenciaAt = potenciaAt/amostra; // média das potências 
  if (potenciaAt<0)potenciaAt = potenciaAt*-1; // se a potência for negativa transforma-a em positiva
        
  //Gravando Valores
        
  if((Vex) == 16)
  {
    GraV1[P1]=equacao(Ptensao);
    GraC1[P1]=equacao(Pcorrente);
    GraP1[P1]=potenciaAt;
    P1++;
    Vex = 0;
    if (P1 == 12)
    {
      P1=0;
      GraV2[P2] =media(GraV1, 15);
      GraC2[P2] =media(GraC1, 15);
      GraP2[P2] =media(GraP1, 15); 
      P2++;  
      if (P2 == 15)
      { 
        P2 = 0;
        Serial.print(rtc.getDateStr(FORMAT_SHORT)); // DATA
        Serial.print(",");
        Serial.print(rtc.getTimeStr()); // HORA
        Serial.print(",");
        Serial.print(String(media(GraV2, 15)));
        Serial.print(",");
        Serial.print(String(media(GraC2, 15)));
        Serial.print(",");
        Serial.print(String(media(GraP2, 15)));
        Serial.println(",4");
        Serial.println(rtc.getTimeStr());
               /* //Imprimindo valor de 3 em 3 segundos
		            Dados = SD.open("Dados.txt", FILE_WRITE);
                Dados.print(rtc.getDateStr(FORMAT_SHORT)); // DATA
                Dados.print(",");
                Dados.print(rtc.getTimeStr()); // HORA
                Dados.print(",");
                Dados.print(String(media(GraV2, 15)));
                Dados.print(",");
                Dados.print(String(media(GraC2, 15)));
                Dados.print(",");
                Dados.print(String(media(GraP2, 15)));
                Dados.println(",4");
                Dados.close();
                Serial.println(rtc.getTimeStr());*/
/*
                 P3 ++;
                 
                 if (P3 == 50)//200
                   {
                     P3=0;
                     //GraV4[P4] =media(GraV3, 50);
                     //GraC4[P4] =media(GraV3, 50);
                     P4 ++;
                   }*/
       }
     }
   }
  
 Vex++;
	
}

float equacao(float *P)
{
	float Veficaz=0;    // Cálculo do Valor RMS
	for (int x=0;x<amostra;x++)
		Veficaz = Veficaz + (*(P+x))*(*(P+x));
	Veficaz = sqrt(Veficaz/amostra);
	return Veficaz;
}

float media(float *P, int num) // Cálculo da Média
{
  float Media = 0;
  for (int y=0;y<num;y++)
  {
    Media = Media + (*(P+y));
  }
  return (Media/num);
}

//FIM

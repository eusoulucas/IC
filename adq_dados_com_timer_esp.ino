hw_timer_t *timer = NULL; /*faz o controle do temporizador (interrupção por tempo)*/
/* Programa para ler e armezenar os valores de corrente e tensão no cartão de memória */

byte senC = 34; //Porta sensor de corrente
byte senT = 35; //Porta sensor de tensão

int zeroC = 512; // Variavel para ajuste de offset dos sensores
int zeroT = 512;

double corrente = 0;
double tensao = 0;

int tme;
int tempo;

long interrupcao = 10000; //Definição do período de amostragem (1/frequencia) em us - 100 p/ 10 KHz

void Tvetor()
{   
  tme = millis(); //tempo inicial do loop
  //Calculando tensão do sensor de corrente
  corrente = analogRead(senC); //Realizando ajuste offset
  corrente = corrente * 0.0008056;

  //Calculando tensão do sensor de tensão
  tensao = analogRead(senT);
  tensao = tensao * 0.0008056;

  Serial.println(corrente);
  Serial.println(tensao);
  Serial.println(tme);
}

void setup() 
{
  Serial.begin(500000);
  pinMode(senT,INPUT); //Configurando os pinos das entradas analógicas
  pinMode(senC,INPUT);

  timer = timerBegin(0, 80, true); //timerID 0, div 80
  //timer, callback, interrupção de borda
  timerAttachInterrupt(timer, Tvetor, true);
  //timer, tempo (us), repetição
  timerAlarmWrite(timer, 10000 , true); // Nosso periodo = 1000us, portanto  a frequência = 1kH
  //timerAlarmEnable(timer); //habilita a interrupção
}

void loop() 
{
  Serial.println("mkoadsm");
}

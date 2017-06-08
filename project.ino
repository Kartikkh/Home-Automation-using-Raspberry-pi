#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "printf.h"


RF24 radio(9,10);


void setup(void){
  while(!Serial);
  Serial.begin(9600);

  radio.begin();

  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  const uint64_t pipe = 0xE8E8F0F0E1LL;
  radio.openReadingPipe(1,pipe);

  radio.enableDynamicPayloads();
  radio.powerUp(); 
  
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  digitalWrite(3,HIGH);
  digitalWrite(4,HIGH);
  digitalWrite(5,HIGH);
  digitalWrite(6,HIGH);
}

void loop(void){
   radio.startListening();
   Serial.println("Starting loop.Radio on.");
   char recievedMessage[32] = {0};
   if(radio.available()){
    radio.read(recievedMessage , sizeof(recievedMessage));
    Serial.println(recievedMessage);
    Serial.println("Turning off th Radio.");
    radio.stopListening(); 
    String stringMessage(recievedMessage);
    Serial.println(stringMessage);
    delay(1000);
    if(stringMessage == "0"){
      digitalWrite(3,HIGH);
      Serial.println("Relay On");
    }
    
    if(stringMessage == "1"){
      digitalWrite(3,LOW);
      Serial.println("Relay Off");
    }
    
    if(stringMessage == "2"){
       digitalWrite(4,LOW);
      Serial.println("Relay On");
    }
    
    if(stringMessage == "3"){
       digitalWrite(4,HIGH);
      Serial.println("Relay Off");
    }
    
   }
   delay(200);
} 

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN

const byte address[6] = "00001";
String hello = ""; 
char incomingByte = 0; 
void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}
void loop() {
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    hello += incomingByte;
    if(hello.length() > 1){
     if(hello[hello.length()-1] == 's' || hello[hello.length()-1] == 'm' || hello[hello.length()-1] == 'p'){
           Serial.println(hello);  
           char char_array[hello.length() + 1];
           hello.toCharArray(char_array, hello.length()+1);
           radio.write(&char_array,sizeof(char_array));
           hello = "";

      }
     if(hello.length() == 7){
      hello = ""; 
     }
    }
   }
}

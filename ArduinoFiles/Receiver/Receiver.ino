#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>

RF24 radio(7, 8); // CE, CSN

const byte address[6] = "00001";

Servo myservo;
const int solenoid_pin = 3;
const int motor_A = 2; 
const int motor_B = 4; 
const int servo_pin = 9; 
const int safety_button = 5;  

void setup() {
  Serial.begin(9600);
  pinMode(motor_A, OUTPUT); 
  pinMode(motor_B, OUTPUT);
  pinMode(solenoid_pin, OUTPUT);
  pinMode(safety_button, INPUT); 
  myservo.attach(servo_pin); 
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  myservo.write(90); 
}

void loop() {
  if (radio.available()) {
    char text[7] = "";
    radio.read(&text, sizeof(text));
    String s; 
    for(int i = 0; i<7; i++){
      if(text[i] == 's'){
         myservo.write(s.toInt());
      }else if(text[i] == 'm'){
        digitalWrite(motor_A, s.toInt()); 
        digitalWrite(motor_B, s.toInt());
      }else if(text[i] == 'p'){
        Serial.println(text); 
        digitalWrite(solenoid_pin, s.toInt()); 
      }
      else{
        s+=text[i];
      }
    }
  }
}

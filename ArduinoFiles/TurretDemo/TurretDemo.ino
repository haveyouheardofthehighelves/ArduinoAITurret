#include <Servo.h>
const int solenoid_pin = 3;
const int motor_A = 2; 
const int motor_B = 4; 
const int servo_pin = 9; 
const int safety_button = 5; 
bool button_pressed = false; 
bool on = false; 
Servo myservo; 

void shoot_solenoid(); 
void start_motors(); 
void stop_everything(); 
void turn_shoot(int angle); 
void setup() {
  myservo.attach(servo_pin); 
  pinMode(motor_A, OUTPUT); 
  pinMode(motor_B, OUTPUT);
  pinMode(solenoid_pin, OUTPUT);
  pinMode(safety_button, INPUT); 
  Serial.begin(9600); 
  // put your setup code here, to run once:

}

void loop() {
    bool button_status = digitalRead
    (safety_button); 
    if (button_status){ 
      button_pressed = true; 
    }
    if(button_pressed && !button_status){ 
      on = !on;  
      button_pressed = false; 
      if(on){
        start_motors(); 
      }
    }
   if(on){
      turn_shoot(90); 
      turn_shoot(180); 
      turn_shoot(90); 
      turn_shoot(0); 
   }
 
  Serial.println(button_status); 
  
  // put your main code here, to run repeatedly:

}

void shoot_solenoid(){ 
  digitalWrite(solenoid_pin, HIGH); 
  delay(100); 
  digitalWrite(solenoid_pin, LOW); 
  delay(900); 
}

void start_motors(){
  digitalWrite(motor_A, HIGH); 
  digitalWrite(motor_B, HIGH); 
  delay(800); 
}

void stop_everything(){
  digitalWrite(motor_A, LOW); 
  digitalWrite(motor_B, LOW); 
  digitalWrite(solenoid_pin, LOW); 
  myservo.write(90); 
}

void turn_shoot(int angle){
      myservo.write(angle); 
      delay(500); 
      shoot_solenoid(); 
      delay(500);
}

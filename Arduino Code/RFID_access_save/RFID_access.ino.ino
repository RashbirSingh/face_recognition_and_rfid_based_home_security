#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
 
#define SS_PIN 10
#define RST_PIN 9
const int trigPin = 7;
const int echoPin = 6;
int led = 5;
char input;
Servo servo;
int angle = 0;
long duration;
  int distance;


MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
 
void setup() 
{
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(led, OUTPUT);
  Serial.begin(9600);   // Initiate a serial communication
  servo.attach(8);
  servo.write(angle);
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  Serial.println("Approximate your card to the reader...");
  Serial.println();
  delay(2000); 

}
void loop() 
{

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance= duration*0.034/2;
  
  if(Serial.available()){
    input = Serial.read();
    if (input == '1'){
    // Look for new cards
    if ( ! mfrc522.PICC_IsNewCardPresent()) 
    {
      return;
    }
    // Select one of the cards
    if ( ! mfrc522.PICC_ReadCardSerial()) 
    {
      return;
    }
    //Show UID on serial monitor
    Serial.print("UID tag :");
    String content= "";
    byte letter;
    for (byte i = 0; i < mfrc522.uid.size; i++) 
    {
       Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
       Serial.print(mfrc522.uid.uidByte[i], HEX);
       content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
       content.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    Serial.println();
    Serial.print("Message : ");
    content.toUpperCase();
    if (content.substring(1) == "04 B7 8C BA EC 4A 80") //change here the UID of the card/cards that you want to give access
    {
      servo.write(90);
      Serial.println("Authorized access");
      Serial.println();
      delay(3000);
    }
   
   else   {
      servo.write(0);
      Serial.println(" Access denied");
      delay(3000);
      
    }
  }
} 

  if (distance < 7){
    digitalWrite(led, HIGH);
    Serial.print("Distance: ");
    Serial.println(distance);
  }
  else if (distance > 7){
    digitalWrite(led, LOW);
    Serial.print("Distance: ");
    Serial.println(distance);
  }
}

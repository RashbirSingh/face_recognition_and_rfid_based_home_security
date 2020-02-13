const int trigPin = 7;
const int echoPin = 6;
int led = 5;

// defines variables
long duration;
int distance;

void setup() {
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
pinMode(led, OUTPUT);
Serial.begin(9600); // Starts the serial communication
}
void loop() {
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distance= duration*0.034/2;
// Prints the distance on the Serial Monitor

if (distance < 6){
  digitalWrite(led, HIGH);
  Serial.print("Distance: ");
  Serial.println(distance);
}
else if (distance > 6){
  digitalWrite(led, LOW);
  Serial.print("Distance: ");
  Serial.println(distance);
}
}

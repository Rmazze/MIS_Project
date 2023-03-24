// This sketch converts voltage into cm for the Sharp IR GP2Y0A41SK0F proximity sensor

// input voltage: 5v
// (4-30cm, analog)


#define sensor1 A0 
#define sensor2 A1 

void setup() {
  Serial.begin(9600); 
}



void loop() {
  
  float volts = analogRead(sensor1)*0.0048828125;  // value from sensor * (5/1024)
  int distance = 13*pow(volts, -1); // worked out from datasheet graph

  int sensorValue = analogRead(sensor2);
  
  Serial.print("Distance:");   // print the distance
  Serial.print(distance);
  Serial.print(",");
  Serial.print("Potentiometer:");   // print the distance
  Serial.println(sensorValue);
  
}
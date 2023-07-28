#define led 13

bool led_state = HIGH;

void setup() {
  Serial.begin(115200);
    
  pinMode(led, OUTPUT);
}

void loop() {
  digitalWrite(led, led_state);    
  delay(1000);
  led_state = !led_state;  
  Serial.print("led_state, ");
  Serial.println(led_state);          
}

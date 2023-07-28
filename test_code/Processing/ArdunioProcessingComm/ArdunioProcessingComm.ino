void setup() {
  // Initialize serial communication with baud rate = 9600
  Serial.begin(9600);
}

void loop() {
  Serial.println("0"); // prints data to the serial port as human-readable ASCII text
  delay(5000); // wait
  Serial.println("1");
  delay(5000);
  Serial.println("0"); // prints data to the serial port as human-readable ASCII text
  delay(5000); // wait
  Serial.println("2");
  delay(5000);
}

#define button 11
#define magnet_led 12
#define magnet 13

bool magnet_state = HIGH;         // the current state of the output pin
bool button_reading;
bool button_state;             // the current reading from the input pin
bool last_button_state = LOW;   // the previous reading from the input pin

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long last_debounce_time = 0;  // the last time the output pin was toggled
unsigned long debounce_delay = 50;    // the debounce time; increase if the output flickers

void setup() {
  pinMode(button, INPUT);
  pinMode(magnet_led, OUTPUT);
  pinMode(magnet, OUTPUT);

  digitalWrite(magnet_led, magnet_state);
  digitalWrite(magnet, magnet_state);
}

void loop() {
  button_reading = digitalRead(button);
  if (button_reading != last_button_state){
    // reset the debouncing timer
    last_debounce_time = millis();
  }

  if ((millis() - last_debounce_time) > debounce_delay){
    if (button_reading != button_state){
      button_state = button_reading;

      // only toggle if the new button state is HIGH
      if (button_state == HIGH){
        magnet_state = !magnet_state;
      }
    }
  }

  digitalWrite(magnet_led, magnet_state);
  digitalWrite(magnet, magnet_state);

  // save the reading. Next time through the loop, it'll be the lastButtonState:
  last_button_state = button_reading;
}

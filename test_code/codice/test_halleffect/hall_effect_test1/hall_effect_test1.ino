/* 
 *  This sketch uses a hall effect sensor as switch to control an LED.
 *  The interrupt technique is used
 *
*/

/*
LOW to trigger the interrupt whenever the pin is low,

CHANGE to trigger the interrupt whenever the pin changes value

RISING to trigger when the pin goes from low to high,

FALLING for when the pin goes from high to low.
 */

#define hall_led 38 //37
#define hall_sens 35 //35
volatile byte hall_led_state = LOW; //important to use volatile variable type here

void setup() {
  pinMode(hall_led, OUTPUT);
  pinMode(hall_sens, INPUT_PULLUP);
  //attachInterrupt(digitalPinToInterrupt(interruptPin), blink, CHANGE);
  attachInterrupt(digitalPinToInterrupt(hall_sens), blink, RISING);
}

void loop() {
  digitalWrite(hall_led, hall_led_state);
}

void blink() {
  //state = !state;
  hall_led_state = !hall_led_state;
}

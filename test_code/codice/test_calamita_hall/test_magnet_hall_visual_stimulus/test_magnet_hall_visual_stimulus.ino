#define hall_sens 2

#define visual_stimulus_led 7

#define ready_button 8
#define reset_button 9

#define ready_led 10
#define hall_led_start 11
#define hall_led_stop 12

#define magnet 13

int program_execution_state = 0;
bool show_results = HIGH;

bool test_ready_state = HIGH;

bool visual_stimulus_led_state = LOW;

bool magnet_state = HIGH;         // the current state of the output pin

bool ready_button_reading;
bool ready_button_state;             // the current reading from the input pin
bool last_ready_button_state = LOW;   // the previous reading from the input pin

unsigned long debounce_delay = 50;    // the debounce time; increase if the output flickers
unsigned long last_debounce_time_ready = 0;  // the last time the output pin was toggled

bool reset_button_reading;
bool reset_button_state;             // the current reading from the input pin
bool last_reset_button_state = LOW;   // the previous reading from the input pin

unsigned long last_debounce_time_reset = 0;  // the last time the output pin was toggled

volatile byte hall_led_start_state = LOW;
volatile byte hall_led_stop_state = LOW;

unsigned long rand_time = 0;
unsigned long stimuly_duration = 3000;
unsigned long test_time_ready = 0;
unsigned long test_time_start = 0;
volatile unsigned long test_time_end = 0;
unsigned long test_elapsed_time = 0;

void setup() {
  Serial.begin(115200);

  pinMode(visual_stimulus_led, OUTPUT);
  
  pinMode(hall_led_start, OUTPUT);
  pinMode(hall_led_stop, OUTPUT);
  pinMode(hall_sens, INPUT_PULLUP);
  
  pinMode(ready_button, INPUT);
  pinMode(reset_button, INPUT);
  
  pinMode(ready_led, OUTPUT);
  pinMode(magnet, OUTPUT);

  digitalWrite(ready_led, test_ready_state);
  digitalWrite(magnet, magnet_state);
  digitalWrite(hall_led_start, hall_led_start_state);
  digitalWrite(hall_led_stop, hall_led_stop_state); 
  digitalWrite(visual_stimulus_led, visual_stimulus_led_state);

  attachInterrupt(digitalPinToInterrupt(hall_sens), stop_test_ISR, RISING);
}

void loop() {
  switch(program_execution_state){
    case(0):  ready_button_reading = digitalRead(ready_button);
              if (ready_button_reading != last_ready_button_state){
                // reset the debouncing timer
                last_debounce_time_ready = millis();
              }

              if ((millis() - last_debounce_time_ready) > debounce_delay){
                if (ready_button_reading != ready_button_state){
                  ready_button_state = ready_button_reading;

                  // only toggle if the new button state is HIGH
                  if (ready_button_state == HIGH){
                    test_time_ready = millis();
                    randomSeed(millis());
                    rand_time = random(5000, 10000);
                    test_ready_state = LOW;
                    program_execution_state = 1;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_ready_button_state = ready_button_reading;
              break;
    case(1):  if ((millis() - test_time_ready) >= rand_time){
                visual_stimulus_led_state = HIGH;
                magnet_state = LOW;
                program_execution_state = 2;
                test_time_start = millis();
                hall_led_start_state = HIGH;
              }
    
              reset_button_reading = digitalRead(reset_button);
              if (reset_button_reading != last_reset_button_state){
                // reset the debouncing timer
                last_debounce_time_reset = millis();
              }

              if ((millis() - last_debounce_time_reset) > debounce_delay){
                if (reset_button_reading != reset_button_state){
                  reset_button_state = reset_button_reading;

                  // only toggle if the new button state is HIGH
                  if (reset_button_state == HIGH){
                    magnet_state = HIGH;
                    hall_led_start_state = LOW;
                    hall_led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state = LOW;
                    program_execution_state = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
              break;
    case(2):  if ((millis() - test_time_start) >= stimuly_duration){
                visual_stimulus_led_state = LOW;
                program_execution_state = 3;  
              }

              reset_button_reading = digitalRead(reset_button);
              if (reset_button_reading != last_reset_button_state){
                // reset the debouncing timer
                last_debounce_time_reset = millis();
              }

              if ((millis() - last_debounce_time_reset) > debounce_delay){
                if (reset_button_reading != reset_button_state){
                  reset_button_state = reset_button_reading;

                  // only toggle if the new button state is HIGH
                  if (reset_button_state == HIGH){
                    magnet_state = HIGH;
                    hall_led_start_state = LOW;
                    hall_led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state = LOW;
                    program_execution_state = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
              break;
    case(3):  reset_button_reading = digitalRead(reset_button);
              if (reset_button_reading != last_reset_button_state){
                // reset the debouncing timer
                last_debounce_time_reset = millis();
              }

              if ((millis() - last_debounce_time_reset) > debounce_delay){
                if (reset_button_reading != reset_button_state){
                  reset_button_state = reset_button_reading;

                  // only toggle if the new button state is HIGH
                  if (reset_button_state == HIGH){
                    magnet_state = HIGH;
                    hall_led_start_state = LOW;
                    hall_led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state = LOW;
                    program_execution_state = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
              break;
    case(4):  test_elapsed_time = test_time_end - test_time_start;
              if (show_results){
                Serial.println("Elapsed time: " + String(test_elapsed_time));
                show_results = LOW;
              }
    
              reset_button_reading = digitalRead(reset_button);
              if (reset_button_reading != last_reset_button_state){
                // reset the debouncing timer
                last_debounce_time_reset = millis();
              }

              if ((millis() - last_debounce_time_reset) > debounce_delay){
                if (reset_button_reading != reset_button_state){
                  reset_button_state = reset_button_reading;

                  // only toggle if the new button state is HIGH
                  if (reset_button_state == HIGH){
                    magnet_state = HIGH;
                    hall_led_start_state = LOW;
                    hall_led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state = LOW;
                    program_execution_state = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
              break;
    default:  test_ready_state = HIGH;
              hall_led_start_state = HIGH;
              hall_led_stop_state = HIGH;

              reset_button_reading = digitalRead(reset_button);
              if (reset_button_reading != last_reset_button_state){
                // reset the debouncing timer
                last_debounce_time_reset = millis();
              }

              if ((millis() - last_debounce_time_reset) > debounce_delay){
                if (reset_button_reading != reset_button_state){
                  reset_button_state = reset_button_reading;

                  // only toggle if the new button state is HIGH
                  if (reset_button_state == HIGH){
                    magnet_state = HIGH;
                    hall_led_start_state = LOW;
                    hall_led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state = LOW;
                    program_execution_state = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
  }
  digitalWrite(ready_led, test_ready_state);
  digitalWrite(magnet, magnet_state);
  digitalWrite(hall_led_start, hall_led_start_state);
  digitalWrite(hall_led_stop, hall_led_stop_state); 
  digitalWrite(visual_stimulus_led, visual_stimulus_led_state);
}

#define hand_sens_sx 11
#define hand_sens_dx 12

#define ready_button 24
#define reset_button 25

#define ready_led 26
#define led_start 27
#define led_stop 28

#define visual_stimulus_led_sx 29
#define visual_stimulus_led_dx 30

#define magnet_sx 31
#define magnet_dx 32

int program_execution_state = 0;
bool show_results = HIGH;

bool test_ready_state = HIGH;

bool visual_stimulus_led_state_sx = LOW;
bool visual_stimulus_led_state_dx = LOW;

bool magnet_state_sx = HIGH;
bool magnet_state_dx = HIGH;

bool ready_button_reading;
bool ready_button_state;             // the current reading from the input pin
bool last_ready_button_state = LOW;   // the previous reading from the input pin

unsigned long debounce_delay = 50;    // the debounce time; increase if the output flickers
unsigned long last_debounce_time_ready = 0;  // the last time the output pin was toggled

bool reset_button_reading;
bool reset_button_state;             // the current reading from the input pin
bool last_reset_button_state = LOW;   // the previous reading from the input pin

unsigned long last_debounce_time_reset = 0;  // the last time the output pin was toggled

volatile byte led_start_state = LOW;
volatile byte led_stop_state = LOW;

unsigned long rand_time = 0;
unsigned long stimuly_duration = 3000;
unsigned long test_time_ready = 0;
unsigned long test_time_start = 0;
volatile unsigned long test_time_end_sx = 0;
volatile unsigned long test_time_end_dx = 0;
unsigned long test_elapsed_time_sx = 0;
unsigned long test_elapsed_time_dx = 0;

bool ongoing_test_sx = LOW;
bool ongoing_test_dx = LOW; 

int test_type = 0; //0 only sx, 1 only dx, 2 both sx and dx

void setup() {
  //Serial.begin(115200);

  pinMode(visual_stimulus_led_sx, OUTPUT);
  pinMode(visual_stimulus_led_dx, OUTPUT);
  
  pinMode(led_start, OUTPUT);
  pinMode(led_stop, OUTPUT);
  pinMode(hand_sens_sx, INPUT_PULLUP);
  pinMode(hand_sens_dx, INPUT_PULLUP);
  
  pinMode(ready_button, INPUT);
  pinMode(reset_button, INPUT);
  
  pinMode(ready_led, OUTPUT);
  pinMode(magnet_sx, OUTPUT);
  pinMode(magnet_dx, OUTPUT);

  digitalWrite(ready_led, test_ready_state);
  digitalWrite(magnet_sx, magnet_state_sx);
  digitalWrite(magnet_dx, magnet_state_dx);
  digitalWrite(led_start, led_start_state);
  digitalWrite(led_stop, led_stop_state); 
  digitalWrite(visual_stimulus_led_sx, visual_stimulus_led_state_sx);
  digitalWrite(visual_stimulus_led_dx, visual_stimulus_led_state_dx);

  attachInterrupt(digitalPinToInterrupt(hand_sens_sx), stop_test_ISR_sx, RISING);
  attachInterrupt(digitalPinToInterrupt(hand_sens_dx), stop_test_ISR_dx, RISING);
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
                    test_type = random(0, 3);
                    Serial.println("Test type: " + String(test_type));
                    switch(test_type){
                      case(0): ongoing_test_sx = HIGH; break;
                      case(1): ongoing_test_dx = HIGH; break;
                      case(2): ongoing_test_sx = HIGH; ongoing_test_dx = HIGH; break;
                      default: ongoing_test_sx = LOW; ongoing_test_dx = LOW;
                    }
                    test_ready_state = LOW;
                    program_execution_state = 1;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_ready_button_state = ready_button_reading;
              break;
    case(1):  if ((millis() - test_time_ready) >= rand_time){
                switch(test_type){
                  case(0): visual_stimulus_led_state_sx = HIGH; 
                           magnet_state_sx = LOW;
                           break;
                  case(1): visual_stimulus_led_state_dx = HIGH; 
                           magnet_state_dx = LOW;
                           break;
                  case(2): visual_stimulus_led_state_sx = HIGH;
                           visual_stimulus_led_state_dx = HIGH;  
                           magnet_state_sx = LOW;
                           magnet_state_dx = LOW;
                           break;
                  default: visual_stimulus_led_state_sx = LOW;
                           visual_stimulus_led_state_dx = LOW;  
                           magnet_state_sx = HIGH;
                           magnet_state_dx = HIGH;
                           break;
                }
                program_execution_state = 2;
                test_time_start = millis();
                led_start_state = HIGH;
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
                    magnet_state_sx = HIGH;
                    magnet_state_dx = HIGH;
                    led_start_state = LOW;
                    led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state_sx = LOW;
                    visual_stimulus_led_state_dx = LOW;
                    program_execution_state = 0;
                    ongoing_test_sx = LOW;
                    ongoing_test_dx = LOW;
                    test_time_ready = 0;
                    test_time_start = 0;
                    test_time_end_sx = 0;
                    test_time_end_dx = 0;
                    test_elapsed_time_sx = 0;
                    test_elapsed_time_dx = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
              break;
    case(2):  if ((millis() - test_time_start) >= stimuly_duration){
                switch(test_type){
                  case(0): visual_stimulus_led_state_sx = LOW; break;
                  case(1): visual_stimulus_led_state_dx = LOW; break;
                  case(2): visual_stimulus_led_state_sx = LOW; visual_stimulus_led_state_dx = LOW; break;
                  default: visual_stimulus_led_state_sx = LOW; visual_stimulus_led_state_dx = LOW;
                }
                program_execution_state = 3;  
              }

              if (ongoing_test_sx == LOW && ongoing_test_dx == LOW){
                visual_stimulus_led_state_sx = LOW;
                visual_stimulus_led_state_dx = LOW;
                led_start_state = LOW;
                led_stop_state = HIGH;
                program_execution_state = 4;
              }
              else if (ongoing_test_sx == LOW){
                visual_stimulus_led_state_sx = LOW;
              }
              else if (ongoing_test_dx == LOW){
                visual_stimulus_led_state_dx = LOW;
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
                    magnet_state_sx = HIGH;
                    magnet_state_dx = HIGH;
                    led_start_state = LOW;
                    led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state_sx = LOW;
                    visual_stimulus_led_state_dx = LOW;
                    program_execution_state = 0;
                    ongoing_test_sx = LOW;
                    ongoing_test_dx = LOW;
                    test_time_ready = 0;
                    test_time_start = 0;
                    test_time_end_sx = 0;
                    test_time_end_dx = 0;
                    test_elapsed_time_sx = 0;
                    test_elapsed_time_dx = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
              break;
    case(3):  reset_button_reading = digitalRead(reset_button);
              if (ongoing_test_sx == LOW && ongoing_test_dx == LOW){
                visual_stimulus_led_state_sx = LOW;
                visual_stimulus_led_state_dx = LOW;
                led_start_state = LOW;
                led_stop_state = HIGH;
                program_execution_state = 4;
              }
              else if (ongoing_test_sx == LOW){
                visual_stimulus_led_state_sx = LOW;
              }
              else if (ongoing_test_dx == LOW){
                visual_stimulus_led_state_dx = LOW;
              }

              if (reset_button_reading != last_reset_button_state){
                // reset the debouncing timer
                last_debounce_time_reset = millis();
              }

              if ((millis() - last_debounce_time_reset) > debounce_delay){
                if (reset_button_reading != reset_button_state){
                  reset_button_state = reset_button_reading;

                  // only toggle if the new button state is HIGH
                  if (reset_button_state == HIGH){
                    magnet_state_sx = HIGH;
                    magnet_state_dx = HIGH;
                    led_start_state = LOW;
                    led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state_sx = LOW;
                    visual_stimulus_led_state_dx = LOW;
                    program_execution_state = 0;
                    ongoing_test_sx = LOW;
                    ongoing_test_dx = LOW;
                    test_time_ready = 0;
                    test_time_start = 0;
                    test_time_end_sx = 0;
                    test_time_end_dx = 0;
                    test_elapsed_time_sx = 0;
                    test_elapsed_time_dx = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
              break;
    case(4):  switch(test_type){
                case(0): test_elapsed_time_sx = test_time_end_sx - test_time_start; break;
                case(1): test_elapsed_time_dx = test_time_end_dx - test_time_start; break;
                case(2): test_elapsed_time_sx = test_time_end_sx - test_time_start; 
                         test_elapsed_time_dx = test_time_end_dx - test_time_start;
                         break;
                default: test_elapsed_time_sx = 0; 
                         test_elapsed_time_dx = 0;
                         break;
              }

              if (show_results){
                Serial.println("Elapsed time sx: " + String(test_elapsed_time_sx));
                Serial.println("Elapsed time dx: " + String(test_elapsed_time_dx));
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
                    magnet_state_sx = HIGH;
                    magnet_state_dx = HIGH;
                    led_start_state = LOW;
                    led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state_sx = LOW;
                    visual_stimulus_led_state_dx = LOW;
                    program_execution_state = 0;
                    ongoing_test_sx = LOW;
                    ongoing_test_dx = LOW;
                    test_time_ready = 0;
                    test_time_start = 0;
                    test_time_end_sx = 0;
                    test_time_end_dx = 0;
                    test_elapsed_time_sx = 0;
                    test_elapsed_time_dx = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
              break;
    default:  test_ready_state = HIGH;
              led_start_state = HIGH;
              led_stop_state = HIGH;

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
                    magnet_state_sx = HIGH;
                    magnet_state_dx = HIGH;
                    led_start_state = LOW;
                    led_stop_state = LOW;
                    show_results = HIGH;
                    test_ready_state = HIGH;
                    visual_stimulus_led_state_sx = LOW;
                    visual_stimulus_led_state_dx = LOW;
                    program_execution_state = 0;
                    ongoing_test_sx = LOW;
                    ongoing_test_dx = LOW;
                    test_time_ready = 0;
                    test_time_start = 0;
                    test_time_end_sx = 0;
                    test_time_end_dx = 0;
                    test_elapsed_time_sx = 0;
                    test_elapsed_time_dx = 0;
                  }
                }
              }
              // save the reading. Next time through the loop, it'll be the lastButtonState:
              last_reset_button_state = reset_button_reading;
  }
  digitalWrite(ready_led, test_ready_state);
  digitalWrite(magnet_sx, magnet_state_sx);
  digitalWrite(magnet_dx, magnet_state_dx);
  digitalWrite(led_start, led_start_state);
  digitalWrite(led_stop, led_stop_state); 
  digitalWrite(visual_stimulus_led_sx, visual_stimulus_led_state_sx);
  digitalWrite(visual_stimulus_led_dx, visual_stimulus_led_state_dx);
}

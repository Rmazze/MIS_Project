// Sensors to see when you chatch the ball
#define hand_sens_sx 11
#define hand_sens_dx 12

// Sensors to see if the hands are in the correct position to begin the test
#define hand_in_position_sx 36
#define hand_in_position_dx 35
// Leds to indicate if the hands are in the correct position to begin the test
#define hand_in_position_sx_led 38
#define hand_in_position_dx_led 37

// Buttons to start and stop the test
#define ready_button 24
#define reset_button 25

// Leds to show in which state the program is
#define ready_led 26
#define led_start 27
#define led_stop 28

// Output for the visial and tactile stimulus
#define visual_stimulus_led_sx 29
#define visual_stimulus_led_dx 30
#define tactile_stimulus_actuator_sx 13
#define tactile_stimulus_actuator_dx 14

// The electromagnet that release the balls
#define magnet_sx 31
#define magnet_dx 32

// Indicate in which state of the state machine the program is
int program_execution_state = 0;

// Indicate if the results must be printed
bool show_results = HIGH;

// Indicate if all is ok and the test can start
bool test_ready_state = HIGH;

// Indicate if the program have to activate the sx or rx stimuli
bool stimulus_sx = LOW;
bool stimulus_dx = LOW;

// Variable received to select which stimuli to use in the test
int stimuli_type = 4; // arrive from python
// Variables that indicate if a stimulus have to be activated or not
bool visual_stimuli = LOW;
bool auditory_stimuli = LOW;
bool tactile_stimuli = LOW;

// Indicate if the user has chatch the ball or not
bool glove_state_sx = HIGH;
bool glove_state_dx = HIGH;

// Indicate if the hands of the user are in the correct position to begin the test
bool hand_in_position_state_sx = HIGH;
bool hand_in_position_state_dx = HIGH; 

// Debounce delay to wait
unsigned long debounce_delay = 50;    // the debounce time; increase if the output flickers

// Variables to read the ready button
bool ready_button_reading;
bool ready_button_state;             
bool last_ready_button_state = LOW;   
unsigned long last_debounce_time_ready = 0;  

// Variables to read the reset button 
bool reset_button_reading;
bool reset_button_state;             
bool last_reset_button_state = LOW;   
unsigned long last_debounce_time_reset = 0; 

// Variables for the state of the leds that show us the execution state of the program
volatile byte led_start_state = LOW; //can remove volatile?
volatile byte led_stop_state = LOW;

// Random time to wait before releasing the ball
unsigned long rand_time = 0;
// How long are the stimuli to produce
unsigned long stimuly_duration = 3000; //decrese this value
// Time after which we consider that the user was not able to catch the balls
unsigned long to_much_time_elapsed = 10000; //decrese this value
// Saves the timestamp in which the test starts
unsigned long test_time_ready = 0;
// Saves the timestamp in which the ball is released
unsigned long test_time_start = 0;
// Save the timestamp in which the ball is chatched
volatile unsigned long test_time_end_sx = 0;
volatile unsigned long test_time_end_dx = 0;
// Contain the difference between test_time_end and test_time_start
unsigned long test_elapsed_time_sx = 0;
unsigned long test_elapsed_time_dx = 0;

// Tell if we are executing the test for sx or dx hand
bool ongoing_test_sx = LOW;
bool ongoing_test_dx = LOW; 
// Select the test type to execute (0: only sx, 1: only dx, 2: both sx and dx)
int test_type = 0; 

void setup() {
  //Serial.begin(115200);
  // pin initialization
  pinMode(visual_stimulus_led_sx, OUTPUT);
  pinMode(visual_stimulus_led_dx, OUTPUT);
  pinMode(tactile_stimulus_actuator_sx, OUTPUT);
  pinMode(tactile_stimulus_actuator_dx, OUTPUT);
  
  pinMode(led_start, OUTPUT);
  pinMode(led_stop, OUTPUT);
  pinMode(hand_sens_sx, INPUT_PULLUP);
  pinMode(hand_sens_dx, INPUT_PULLUP);

  pinMode(hand_in_position_sx, INPUT);
  pinMode(hand_in_position_dx, INPUT);
  pinMode(hand_in_position_sx_led, OUTPUT);
  pinMode(hand_in_position_dx_led, OUTPUT);
  
  pinMode(ready_button, INPUT);
  pinMode(reset_button, INPUT);
  
  pinMode(ready_led, OUTPUT);
  pinMode(magnet_sx, OUTPUT);
  pinMode(magnet_dx, OUTPUT);

  // output some values
  digitalWrite(ready_led, test_ready_state);
  digitalWrite(magnet_sx, glove_state_sx);
  digitalWrite(magnet_dx, glove_state_dx);
  digitalWrite(led_start, led_start_state);
  digitalWrite(led_stop, led_stop_state); 
  digitalWrite(visual_stimulus_led_sx, stimulus_sx);
  digitalWrite(visual_stimulus_led_dx, stimulus_dx);

  // interupt initialization
  attachInterrupt(digitalPinToInterrupt(hand_sens_sx), stop_test_ISR_sx, RISING);
  attachInterrupt(digitalPinToInterrupt(hand_sens_dx), stop_test_ISR_dx, RISING);

  Serial.println("Select stimuli");
  // select which stimuli to use for this test
  select_stimuli(stimuli_type, visual_stimuli, auditory_stimuli, tactile_stimuli);
}

void loop() {
  // read if hands are in the correct position
  hand_in_position_state_sx = digitalRead(hand_in_position_sx);
  hand_in_position_state_dx = digitalRead(hand_in_position_dx);
  switch(program_execution_state){
    // wait the user to be ready
    case(0):  //Serial.println("Case 0: ");
              // wait for hands of the user to be in the correct position
              if ((hand_in_position_state_sx == LOW) && (hand_in_position_state_dx == LOW)){
                led_start_state = LOW;
                led_stop_state = LOW;
                stimulus_sx = LOW;
                stimulus_dx = LOW;
                program_execution_state = 1;
              }      
              break;    
    // wait the signal to start the test and select the test to execute
    case(1):  //Serial.println("Case 1: ");
              // read ready button state
              // andwait for the ready signal to begin the test
              ready_button_reading = digitalRead(ready_button);
              if (ready_button_reading != last_ready_button_state){
                last_debounce_time_ready = millis();
              }

              if ((millis() - last_debounce_time_ready) > debounce_delay){
                if (ready_button_reading != ready_button_state){
                  ready_button_state = ready_button_reading;

                  if (ready_button_state == HIGH){
                    // select randomly the balls to release in the test
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
                    // test is starteded
                    test_ready_state = LOW;
                    // go to next state
                    program_execution_state = 2;
                  }
                }
              }
              last_ready_button_state = ready_button_reading;

              // check that hands are still in the right position in position
              if ((hand_in_position_state_sx == HIGH) || (hand_in_position_state_dx == HIGH)){
                program_execution_state = -1;
                Serial.println("Hands not in position: ");
              }
    
              //reset code
              //reset_button_reading = digitalRead(reset_button);
              //if (reset_button_reading != last_reset_button_state){
              //  last_debounce_time_reset = millis();
              //}
//
              //if ((millis() - last_debounce_time_reset) > debounce_delay){
              //  if (reset_button_reading != reset_button_state){
              //    reset_button_state = reset_button_reading;
//
              //    if (reset_button_state == HIGH){
              //      program_execution_state = -1; 
              //    }
              //  }
              //}
              //last_reset_button_state = reset_button_reading;
              read_reset_button(reset_button_reading, 
                                reset_button_state, 
                                last_reset_button_state, 
                                last_debounce_time_reset,
                                debounce_delay,
                                program_execution_state);

              break;
    // wait a random time before releasing the balls
    case(2):  //Serial.println("Case 2: ");
              // wait a random time than release the selected balls
              if ((millis() - test_time_ready) >= rand_time){
                switch(test_type){
                  case(0): stimulus_sx = HIGH; 
                           glove_state_sx = LOW;
                           break;
                  case(1): stimulus_dx = HIGH; 
                           glove_state_dx = LOW;
                           break;
                  case(2): stimulus_sx = HIGH;
                           stimulus_dx = HIGH;  
                           glove_state_sx = LOW;
                           glove_state_dx = LOW;
                           break;
                  default: stimulus_sx = LOW;
                           stimulus_dx = LOW;  
                           glove_state_sx = HIGH;
                           glove_state_dx = HIGH;
                           break;
                }
                program_execution_state = 3;
                test_time_start = millis();
                led_start_state = HIGH;
              }

              //check hands in position
              if ((hand_in_position_state_sx == HIGH) || (hand_in_position_state_dx == HIGH)){
                program_execution_state = -1;
                Serial.println("Hands not in position: ");
              }
    
              //reset code
              //reset_button_reading = digitalRead(reset_button);
              //if (reset_button_reading != last_reset_button_state){
              //  last_debounce_time_reset = millis();
              //}
//
              //if ((millis() - last_debounce_time_reset) > debounce_delay){
              //  if (reset_button_reading != reset_button_state){
              //    reset_button_state = reset_button_reading;
//
              //    if (reset_button_state == HIGH){
              //      program_execution_state = -1; 
              //    }
              //  }
              //}
              //last_reset_button_state = reset_button_reading;
              read_reset_button(reset_button_reading, 
                                reset_button_state, 
                                last_reset_button_state, 
                                last_debounce_time_reset,
                                debounce_delay,
                                program_execution_state);
              break;
    // see if the user chatches all the balls and turn off the stimuli if it chatches or enough tie is last
    case(3):  //Serial.println("Case 3: ");
              // turn off stimuli if enought time is last than go to next state
              if ((millis() - test_time_start) >= stimuly_duration){
                switch(test_type){
                  case(0): stimulus_sx = LOW; break;
                  case(1): stimulus_dx = LOW; break;
                  case(2): stimulus_sx = LOW; stimulus_dx = LOW; break;
                  default: stimulus_sx = LOW; stimulus_dx = LOW;
                }
                program_execution_state = 4;  
              }

              // turn off stimulus when user chatches the right ball
              // when all released balls are cheched jump to state 5
              if (ongoing_test_sx == LOW && ongoing_test_dx == LOW){
                stimulus_sx = LOW;
                stimulus_dx = LOW;
                led_start_state = LOW;
                led_stop_state = HIGH;
                Serial.println("Produce happy sound");
                program_execution_state = 5;
              }
              else if (ongoing_test_sx == LOW){
                stimulus_sx = LOW;
              }
              else if (ongoing_test_dx == LOW){
                stimulus_dx = LOW;
              }

              //reset code
              //reset_button_reading = digitalRead(reset_button);
              //if (reset_button_reading != last_reset_button_state){
              //  last_debounce_time_reset = millis();
              //}
//
              //if ((millis() - last_debounce_time_reset) > debounce_delay){
              //  if (reset_button_reading != reset_button_state){
              //    reset_button_state = reset_button_reading;
//
              //    if (reset_button_state == HIGH){
              //      program_execution_state = -1; 
              //    }
              //  }
              //}
              //last_reset_button_state = reset_button_reading;
              read_reset_button(reset_button_reading, 
                                reset_button_state, 
                                last_reset_button_state, 
                                last_debounce_time_reset,
                                debounce_delay,
                                program_execution_state);
              break;
    // see if the user chatches all the balls, if too much time is elapesed consider as the user didn't chatch the balls
    case(4):  //Serial.println("Case 4: ");
              // when all released balls are cheched go to next state
              if (ongoing_test_sx == LOW && ongoing_test_dx == LOW){
                stimulus_sx = LOW;
                stimulus_dx = LOW;
                led_start_state = LOW;
                led_stop_state = HIGH;
                Serial.println("Produce happy sound");
                program_execution_state = 5;
              }
              else if (ongoing_test_sx == LOW){
                stimulus_sx = LOW;
              }
              else if (ongoing_test_dx == LOW){
                stimulus_dx = LOW;
              }

              // too much time is elapsed, consider as the user didn't chanch the balls
              if ((millis() - test_time_start) >= to_much_time_elapsed){
                Serial.println("Produce sad sound");
                // may add something to communicate fake times?
                program_execution_state = -1;  
              }
              

              //reset code
              //reset_button_reading = digitalRead(reset_button);
              //if (reset_button_reading != last_reset_button_state){
              //  last_debounce_time_reset = millis();
              //}
//
              //if ((millis() - last_debounce_time_reset) > debounce_delay){
              //  if (reset_button_reading != reset_button_state){
              //    reset_button_state = reset_button_reading;
//
              //    if (reset_button_state == HIGH){
              //      program_execution_state = -1; 
              //    }
              //  }
              //}
              //last_reset_button_state = reset_button_reading;
              read_reset_button(reset_button_reading, 
                                reset_button_state, 
                                last_reset_button_state, 
                                last_debounce_time_reset,
                                debounce_delay,
                                program_execution_state);
              break;
    // compute results of this execution
    case(5):  //Serial.println("Case 5: ");
              switch(test_type){
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

              //reset code
              //reset_button_reading = digitalRead(reset_button);
              //if (reset_button_reading != last_reset_button_state){
              //  last_debounce_time_reset = millis();
              //}
//
              //if ((millis() - last_debounce_time_reset) > debounce_delay){
              //  if (reset_button_reading != reset_button_state){
              //    reset_button_state = reset_button_reading;
//
              //    if (reset_button_state == HIGH){
              //      program_execution_state = -1; 
              //    }
              //  }
              //}
              //last_reset_button_state = reset_button_reading;
              read_reset_button(reset_button_reading, 
                                reset_button_state, 
                                last_reset_button_state, 
                                last_debounce_time_reset,
                                debounce_delay,
                                program_execution_state);
              break;
    // reset state
    default:  //Serial.println("Case default: ");
              glove_state_sx = HIGH; //reset state
              glove_state_dx = HIGH;
              led_start_state = HIGH; //LOW;
              led_stop_state = HIGH; //LOW;
              show_results = HIGH;
              test_ready_state = HIGH;
              stimulus_sx = HIGH; //LOW;
              stimulus_dx = HIGH; //LOW;
              program_execution_state = 0;
              ongoing_test_sx = LOW;
              ongoing_test_dx = LOW;
              test_time_ready = 0;
              test_time_start = 0;
              test_time_end_sx = 0;
              test_time_end_dx = 0;
              test_elapsed_time_sx = 0;
              test_elapsed_time_dx = 0;

              program_execution_state = 0;
  }
  // produce outputs
  produce_stimuli(stimulus_sx, stimulus_dx, visual_stimuli, auditory_stimuli, tactile_stimuli);
  digitalWrite(ready_led, test_ready_state);
  digitalWrite(magnet_sx, glove_state_sx);
  digitalWrite(magnet_dx, glove_state_dx);
  digitalWrite(led_start, led_start_state);
  digitalWrite(led_stop, led_stop_state); 
  digitalWrite(hand_in_position_sx_led, (1-hand_in_position_state_sx));
  digitalWrite(hand_in_position_dx_led, (1-hand_in_position_state_dx));
}

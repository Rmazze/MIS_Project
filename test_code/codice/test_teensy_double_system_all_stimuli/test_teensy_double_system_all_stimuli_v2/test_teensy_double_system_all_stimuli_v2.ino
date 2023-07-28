// Sensors to see when you chatch the ball
#define hand_sens_sx 7
#define hand_sens_dx 10

// Sensors to see if the hands are in the correct position to begin the test
#define hand_in_position_sx 23
#define hand_in_position_dx 20
// Leds to indicate if the hands are in the correct position to begin the test
#define hand_in_position_sx_led 24
#define hand_in_position_dx_led 25

// Buttons to start and stop the test
#define reset_button 16

// Leds to show in which state the program is
#define ready_led 26
#define led_start 27
#define led_stop 28

// Output for the visial and tactile stimulus
#define visual_stimulus_led_sx 29
#define visual_stimulus_led_dx 30
#define tactile_stimulus_actuator_sx 31
#define tactile_stimulus_actuator_dx 32

// The electromagnet that release the balls
#define magnet_sx 11
#define magnet_dx 12

//reboot teensy at the end of a test
#define RESTART_ADDR       0xE000ED0C
#define READ_RESTART()     (*(volatile uint32_t *)RESTART_ADDR)
#define WRITE_RESTART(val) ((*(volatile uint32_t *)RESTART_ADDR) = (val))

// Indicate in which state of the state machine the program is and if we are already in a test loop
int program_execution_state = 0;
bool execution = LOW; //can be removed? seems not to be used

// Indicate if the results must be printed
bool show_results = HIGH;

// Indicate if all is ok and the test can start
bool test_ready_state = LOW;

// Indicate if the program have to activate the sx or rx stimuli
bool stimulus_sx = LOW;
bool stimulus_dx = LOW;

// Variable received to select which stimuli to use in the test
//int stimuli_type = 4; // arrive from python
// Variables that indicate if a stimulus have to be activated or not
bool visual_stimuli = LOW;
bool noaudio_stimuli = LOW;
bool auditory_stimuli = LOW;
bool tactile_stimuli = LOW;

// Indicate if the user has caught the ball or not
bool glove_state_sx = HIGH;
bool glove_state_dx = HIGH;

// Indicate if the hands of the user are in the correct position to begin the test
bool hand_in_position_state_sx = HIGH;
bool hand_in_position_state_dx = HIGH; 

// Debounce delay to wait
unsigned long debounce_delay = 50;    // the debounce time; increase if the output flickers

// Variables to read the reset button 
bool reset_button_reading;
bool reset_button_state;             
bool last_reset_button_state = LOW;   
unsigned long last_debounce_time_reset = 0; 

// Variables for the state of the leds that show us the execution state of the program
//volatile byte led_start_state = HIGH; //can remove volatile?
//volatile byte led_stop_state = HIGH;
bool led_start_state = HIGH;
bool led_stop_state = HIGH;

// Random time to wait before releasing the ball
unsigned long rand_time = 0;
// How long are the stimuli to produce
unsigned long stimuly_duration = 1500; //decrese this value
//delay time before detaching the balls
unsigned long detachment_time= 400;
// Time after which we consider that the user was not able to catch the balls
unsigned long to_much_time_elapsed = 2000; //decrese this value
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


unsigned long result_sx = 0;
unsigned long result_dx = 0;

// Tell if we are executing the test for sx or dx hand
bool ongoing_test_sx = LOW;
bool ongoing_test_dx = LOW; 
// Select the test type to execute (0: only sx, 1: only dx, 2: both sx and dx)
int test_type = 0; 

String received_buffer; // buffer for receiving commands
String reset_buffer;
char commandSerial[10];
bool statecom = false;
bool stateSerial = false;
char reset_buffer_char[10];

// For debugging reasons to avoid unneccessary looping prints
bool first0 = true;
bool first1 = true;
bool first2 = true;
bool first3 = true;
bool first4 = true;
bool first5 = true;
bool first6 = true;
bool first7 = true;
bool first8 = true;
bool first9 = true;
bool firstD = true;

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

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  //Serial.println("Select stimuli");
  // select which stimuli to use for this test
  //select_stimuli(stimuli_type, visual_stimuli, auditory_stimuli, tactile_stimuli);
}

void loop() {
  // read if hands are in the correct position
  hand_in_position_state_sx = digitalRead(hand_in_position_sx);
  hand_in_position_state_dx = digitalRead(hand_in_position_dx);
  if (Serial.available() > 0){
    received_buffer = Serial.readStringUntil('\n');
    Serial.println(received_buffer);
    Serial.flush();
  }
  int str_len = received_buffer.length() + 1; 
  char received_buffer_char[str_len];
  received_buffer.toCharArray(received_buffer_char, str_len);
  if(str_len >= 2){ // 4 is an arbitrary number
    //Serial.println(received_buffer_char); // Print for debugging reasons
    parseCom(received_buffer_char);
    
    Serial.flush();
  }
  if (statecom){
    switch(program_execution_state){
      // wait for the test initialization
        case(0):  if(first0){
                    Serial.println("State 0");
                    first0 = false;
                  }

                  if (commandSerial[0] == '<'){
                    Serial.println("First char <");
                    select_stimuli_regex(commandSerial, visual_stimuli, auditory_stimuli, tactile_stimuli);
                    test_ready_state = HIGH;
                    program_execution_state = 1;
                  }
                  if(commandSerial[1] == 'P'){
                    program_execution_state = 7;
                    Serial.println("SI va nello stato 7: " + commandSerial[0]);
                  }
                  if(commandSerial[1] == 'C'){
                    program_execution_state = 9;
                    Serial.println("SI va nello stato 9: " + commandSerial[0]);
                  }else{
                    Serial.println("First char: " + commandSerial[0]);   
                    //statecom = false; 
                  }

                break;

      // wait the user to be ready
      case(1):  if(first1){
                  Serial.println("State 1 " + tactile_stimuli);
                  first1 = false;
                }

                // wait for hands of the user to be in the correct position
                if ((hand_in_position_state_sx == LOW) && (hand_in_position_state_dx == LOW)){

                  test_time_ready = millis();
                  randomSeed(millis());
                  rand_time = random(5000, 10000);
                  if (tactile_stimuli == HIGH){
                    test_type = 1;
                  }else{
                    test_type = random(0, 2);
                  }
                  switch(test_type){
                      case(0): ongoing_test_sx = HIGH; break;
                      case(1): ongoing_test_dx = HIGH; break;
                      //case(2): ongoing_test_sx = HIGH; ongoing_test_dx = HIGH; break;
                      default: ongoing_test_sx = LOW; ongoing_test_dx = LOW;
                    }
                  // test is starteded
                  test_ready_state = LOW;
                  led_start_state = LOW;
                  led_stop_state = LOW;
                  // go to next state
                  program_execution_state = 2;
                }      

                read_reset_button(reset_button_reading, 
                                  reset_button_state, 
                                  last_reset_button_state, 
                                  last_debounce_time_reset,
                                  debounce_delay,
                                  program_execution_state);

                reset_from_server(received_buffer_char, program_execution_state); 
                break;  

      // wait a random time before releasing the balls
        case(2):if(first2){
                  Serial.println("State 2");
                  first2 = false;
                }

                //check hands in position
                if ((hand_in_position_state_sx == HIGH) || (hand_in_position_state_dx == HIGH)){
                  test_ready_state = HIGH;
                  led_start_state = HIGH;
                  led_stop_state = HIGH;
                  program_execution_state = 8;
                  Serial.println("Hands not in position: ");
                }

                // wait a random time than release the selected balls
                if ((millis() - test_time_ready) >= rand_time){
                  switch(test_type){
                    case(0): stimulus_sx = HIGH; 
                             //glove_state_sx = LOW;
                             break;
                    case(1): stimulus_dx = HIGH; 
                             //glove_state_dx = LOW;
                             break;
                    case(2): stimulus_sx = HIGH;
                             stimulus_dx = HIGH;  
                             //glove_state_sx = LOW;
                             //glove_state_dx = LOW;
                             break;
                    default: stimulus_sx = LOW;
                             stimulus_dx = LOW;  
                             //glove_state_sx = HIGH;
                             //glove_state_dx = HIGH;
                             break;
                  }
                  program_execution_state = 3;
                  test_time_start = millis();
                  //led_start_state = HIGH;
                }

                read_reset_button(reset_button_reading, 
                                  reset_button_state, 
                                  last_reset_button_state, 
                                  last_debounce_time_reset,
                                  debounce_delay,
                                  program_execution_state);

                reset_from_server(received_buffer_char, program_execution_state);  
                break;

      case(3): if(first3){
                  Serial.println("State 3");
                  first3 = false;
                }
      
                if ((millis() - test_time_start) >= detachment_time){
                  switch(test_type){
                    case(0): //stimulus_sx = HIGH; 
                             glove_state_sx = LOW;
                             break;
                    case(1): //stimulus_dx = HIGH; 
                             glove_state_dx = LOW;
                             break;
                    case(2): //stimulus_sx = HIGH;
                             //stimulus_dx = HIGH;  
                             glove_state_sx = LOW;
                             glove_state_dx = LOW;
                             break;
                    default: //stimulus_sx = LOW;
                             //stimulus_dx = LOW;  
                             glove_state_sx = HIGH;
                             glove_state_dx = HIGH;
                             break;
                  }
                  program_execution_state = 4;
                  //test_time_start = millis();
                  //led_start_state = HIGH;
                }
                read_reset_button(reset_button_reading, 
                                  reset_button_state, 
                                  last_reset_button_state, 
                                  last_debounce_time_reset,
                                  debounce_delay,
                                  program_execution_state);

                //if (received_buffer_char[0] == 'R'){ //non ha senso fare lo stesso controllo che viene poi fatto dentro la funzione
                //reset_from_server(received_buffer_char, program_execution_state); 
                //} 
                break;
      
      // see if the user chatches all the balls and turn off the stimuli if it chatches or enough tie is last
      case(4):  if(first4){
                  Serial.println("State 4");
                  first4 = false;
                }

                // turn off stimuli if enought time is last than go to next state
                if ((millis() - test_time_start) >= stimuly_duration){
                //  switch(test_type){
                //    case(0): stimulus_sx = LOW; break;
                //    case(1): stimulus_dx = LOW; break;
                //    case(2): stimulus_sx = LOW; stimulus_dx = LOW; break;
                //    default: stimulus_sx = LOW; stimulus_dx = LOW;
                // }
                  stimulus_sx = LOW;
                  stimulus_dx = LOW;
                  program_execution_state = 5;  
                }

                // turn off stimulus when user chatches the right ball
                // when all released balls are cheched jump to state 5
                if (ongoing_test_sx == LOW && ongoing_test_dx == LOW){
                  stimulus_sx = LOW;
                  stimulus_dx = LOW;
                  led_start_state = LOW;
                  led_stop_state = HIGH;
                  program_execution_state = 5;
                }
                else if (ongoing_test_sx == LOW){
                  stimulus_sx = LOW;
                }
                else if (ongoing_test_dx == LOW){
                  stimulus_dx = LOW;
                }

                read_reset_button(reset_button_reading, 
                                  reset_button_state, 
                                  last_reset_button_state, 
                                  last_debounce_time_reset,
                                  debounce_delay,
                                  program_execution_state);
                                  
                reset_from_server(received_buffer_char, program_execution_state);  
                break;

      // see if the user chatches all the balls, if too much time is elapesed consider as the user didn't chatch the balls
      case(5):  if(first5){
                  Serial.println("State 5");
                  first5 = false;
                }
                
                // when all released balls are cheched go to next state
                if (ongoing_test_sx == LOW && ongoing_test_dx == LOW){
                  led_start_state = LOW;
                  led_stop_state = HIGH;
                  Serial.println("Produce happy sound");
                  program_execution_state = 6;
                }

                // too much time is elapsed, consider as the user didn't chanch the balls
                if ((millis() - test_time_start) >= to_much_time_elapsed){
                  Serial.println("SAD");
                  // may add something to communicate fake times?
                  program_execution_state = -1;  
                }

                read_reset_button(reset_button_reading, 
                                  reset_button_state, 
                                  last_reset_button_state, 
                                  last_debounce_time_reset,
                                  debounce_delay,
                                  program_execution_state);
                reset_from_server(received_buffer_char, program_execution_state); 
                break;

      // compute results of this execution
      case(6):  if(first6){
                  Serial.println("State 6");
                  first6 = false;
                }

                switch(test_type){
                  case(0): test_elapsed_time_sx = test_time_end_sx - test_time_start; break;
                  case(1): test_elapsed_time_dx = test_time_end_dx - test_time_start; break;
                  case(2): test_elapsed_time_sx = test_time_end_sx - test_time_start; 
                           test_elapsed_time_dx = test_time_end_dx - test_time_start;
                           break;
                  default: test_elapsed_time_sx = 0; 
                           test_elapsed_time_dx = 0;
                }

                if (show_results){
                  delay(300);
                  Serial.println("HAP sx:" + String(test_elapsed_time_sx) + "|dx:"+ String(test_elapsed_time_dx));
                  //WRITE_RESTART(0x5FA0004);
                  show_results = false;
                  program_execution_state = -1; //better to use this again
                }

                read_reset_button(reset_button_reading, 
                                  reset_button_state, 
                                  last_reset_button_state, 
                                  last_debounce_time_reset,
                                  debounce_delay,
                                  program_execution_state);
                reset_from_server(commandSerial, program_execution_state); 
                break;

      //test all different stimuli
      case(7): if(first7){
                  Serial.println("State 7");
                  first7 = false;
               }
               if(commandSerial[3] == 'V'){
                Serial.println("Visivo");
                digitalWrite(visual_stimulus_led_sx, HIGH);
                digitalWrite(visual_stimulus_led_dx, HIGH);
                delay(stimuly_duration);
                digitalWrite(visual_stimulus_led_sx, LOW);
                digitalWrite(visual_stimulus_led_dx, LOW);
               } 
               else if (commandSerial[3] == 'T'){
                Serial.println("Tattile");
                digitalWrite(tactile_stimulus_actuator_sx, HIGH);
                digitalWrite(tactile_stimulus_actuator_dx, HIGH);
                delay(stimuly_duration);
                digitalWrite(tactile_stimulus_actuator_sx, LOW);
                digitalWrite(tactile_stimulus_actuator_dx, LOW);
               }
               
               program_execution_state = -1;
               break;

      // reset for when hands not in position
      case(8):  if(first8){
                  Serial.println("State 8");
                  first8 = false;
                }
                test_ready_state = LOW;
                led_start_state = LOW;
                led_stop_state = LOW;

                test_time_ready = millis();
                rand_time = random(5000, 10000);

                first2 = true;

                program_execution_state = 2;
                break;

// reset for when hands not in position
      case(9):  if(first9){
                  Serial.println("State 9");
                  first9 = false;
                }

                if (show_results){
                  delay(300);
                  Serial.println("RES sx:" + String(result_sx) + "|dx:"+ String(result_dx));
                  //WRITE_RESTART(0x5FA0004);
                  show_results = false;
                  program_execution_state = -1; //better to use this again
                }

      // reset state that reset everything
      default:  if(firstD){
                  Serial.println("Default state");
                  firstD = false;
                }

                glove_state_sx = HIGH;
                glove_state_dx = HIGH;

                led_start_state = HIGH; //LOW;
                led_stop_state = HIGH; //LOW;
                test_ready_state = LOW;

                show_results = HIGH;

                hand_in_position_state_sx = HIGH;
                hand_in_position_state_dx = HIGH; 

                stimulus_sx = LOW;
                stimulus_dx = LOW;

                ongoing_test_sx = LOW;
                ongoing_test_dx = LOW;

                test_time_ready = 0;
                test_time_start = 0;
                test_time_end_sx = 0;
                test_time_end_dx = 0;
                result_sx = test_elapsed_time_sx;
                result_dx = test_elapsed_time_dx;
                test_elapsed_time_sx = 0;
                test_elapsed_time_dx = 0;
                
                received_buffer = "";
                reset_buffer = "";

                program_execution_state = 0;
                execution = LOW;

                first0 = true;
                first1 = true;
                first2 = true;
                first3 = true;
                first4 = true;
                first5 = true;
                first6 = true;
                first7 = true;
                first8 = true;
                first9 = true;
                firstD = true;
                statecom = false;
                Serial.println("Default state");
    }
    // produce outputs
    produce_stimuli(stimulus_sx, stimulus_dx, visual_stimuli, auditory_stimuli, noaudio_stimuli, tactile_stimuli);
    digitalWrite(ready_led, test_ready_state);
    digitalWrite(magnet_sx, glove_state_sx);
    digitalWrite(magnet_dx, glove_state_dx);
    digitalWrite(led_start, led_start_state);
    digitalWrite(led_stop, led_stop_state); 
    digitalWrite(hand_in_position_sx_led, (1-hand_in_position_state_sx));
    digitalWrite(hand_in_position_dx_led, (1-hand_in_position_state_dx));
  }
}

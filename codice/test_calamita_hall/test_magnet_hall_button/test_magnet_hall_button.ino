#define hall_sens 2

#define magnet_button 8
#define reset_button 9

#define magnet_led 10
#define hall_led_start 11
#define hall_led_stop 12

#define magnet 13

int program_execution_state = 0;
bool show_results = HIGH;

bool magnet_state = HIGH;         // the current state of the output pin
bool magnet_button_reading;
bool magnet_button_state;             // the current reading from the input pin
bool last_magnet_button_state = LOW;   // the previous reading from the input pin

unsigned long debounce_delay = 50;    // the debounce time; increase if the output flickers
unsigned long last_debounce_time_magnet = 0;  // the last time the output pin was toggled

bool reset_button_reading;
bool reset_button_state;             // the current reading from the input pin
bool last_reset_button_state = LOW;   // the previous reading from the input pin

unsigned long last_debounce_time_reset = 0;  // the last time the output pin was toggled

volatile byte hall_led_start_state = LOW;
volatile byte hall_led_stop_state = LOW;

unsigned long test_time_start = 0;
volatile unsigned long test_time_end = 0;
unsigned long test_elapsed_time = 0;

void setup() {
  Serial.begin(115200);
  
  pinMode(hall_led_start, OUTPUT);
  pinMode(hall_led_stop, OUTPUT);
  pinMode(hall_sens, INPUT_PULLUP);

  //attachInterrupt(digitalPinToInterrupt(hall_sens), stop_test_ISR, RISING);
  pinMode(reset_button, INPUT);
  pinMode(magnet_button, INPUT);
  pinMode(magnet_led, OUTPUT);
  pinMode(magnet, OUTPUT);

  digitalWrite(magnet_led, magnet_state);
  digitalWrite(magnet, magnet_state);
}

void loop() {
  if (program_execution_state == 0){
    magnet_button_reading = digitalRead(magnet_button);
    if (magnet_button_reading != last_magnet_button_state){
      // reset the debouncing timer
      last_debounce_time_magnet = millis();
    }

    if ((millis() - last_debounce_time_magnet) > debounce_delay){
      if (magnet_button_reading != magnet_button_state){
        magnet_button_state = magnet_button_reading;

        // only toggle if the new button state is HIGH
        if (magnet_button_state == HIGH){
          magnet_state = !magnet_state;
          program_execution_state = 1;
          test_time_start = millis();
          hall_led_start_state = HIGH;
        }
      }
    }
    // save the reading. Next time through the loop, it'll be the lastButtonState:
    last_magnet_button_state = magnet_button_reading;
  }
  else if (program_execution_state == 1){
    attachInterrupt(digitalPinToInterrupt(hall_sens), stop_test_ISR, RISING);
  }
  else if (program_execution_state == 2){
    //print results and wait for reset
    test_elapsed_time = test_time_end - test_time_start;
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
          program_execution_state = 0;
        }
      }
    }
    // save the reading. Next time through the loop, it'll be the lastButtonState:
    last_reset_button_state = reset_button_reading;
  }
  digitalWrite(magnet_led, magnet_state);
  digitalWrite(magnet, magnet_state);
  digitalWrite(hall_led_start, hall_led_start_state);
  digitalWrite(hall_led_stop, hall_led_stop_state); 
}

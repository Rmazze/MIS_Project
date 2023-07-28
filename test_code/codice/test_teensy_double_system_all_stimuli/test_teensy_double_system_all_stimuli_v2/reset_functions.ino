// read reset button
void read_reset_button(bool reset_button_reading, 
                    bool reset_button_state, 
                    bool &last_reset_button_state, 
                    unsigned long &last_debounce_time_reset, 
                    unsigned long debounce_delay,
                    int &program_execution_state){
    reset_button_reading = digitalRead(reset_button);
    if (reset_button_reading != last_reset_button_state){
        last_debounce_time_reset = millis();
    }

    if ((millis() - last_debounce_time_reset) > debounce_delay){
        if (reset_button_reading != reset_button_state){
            reset_button_state = reset_button_reading;
            if (reset_button_state == HIGH){
                program_execution_state = -1;
                Serial.println("esesesesesese");
            }
        }
    }
    last_reset_button_state = reset_button_reading;
}

void reset_from_server(char receivedChars_reset[], int &program_execution_state){    
    if (receivedChars_reset[1] == 'R'){
        program_execution_state = -1;
        Serial.println("resettando");
    } 
}

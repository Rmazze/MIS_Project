// produce the selected stimuli for this test
void produce_stimuli(bool stimulus_sx, bool stimulus_dx, bool visual_stimuli, bool auditory_stimuli, bool noaudio_stimuli,bool tactile_stimuli){
    if (visual_stimuli == HIGH){
        digitalWrite(visual_stimulus_led_sx, stimulus_sx);
        digitalWrite(visual_stimulus_led_dx, stimulus_dx);
        if (stimulus_sx == HIGH || stimulus_dx == HIGH){
          Serial.println("NOTAUD");
        }
    }
    if (auditory_stimuli == HIGH){
        if (stimulus_sx == HIGH && stimulus_dx == HIGH){ 
            Serial.println("AUDXX"); // command to invoke both audio sources
        }
        else if (stimulus_sx == HIGH){
            Serial.println("AUDSX");// command to invoke left audio source
        }
        else if (stimulus_dx == HIGH){
            Serial.println("AUDDX");// command to invoke right audio source
        }
        else{
            //Serial.println("NOTAUD");// command for no audio (never gets considered though)
        }
        
    }
    if (tactile_stimuli == HIGH){
        digitalWrite(tactile_stimulus_actuator_sx, stimulus_sx);
        digitalWrite(tactile_stimulus_actuator_dx, stimulus_dx);
        if (stimulus_sx == HIGH || stimulus_dx == HIGH){
          Serial.println("NOTAUD");
        }
    }  
}

// produce the selected stimuli for this test
void produce_stimuli(bool stimulus_sx, bool stimulus_dx, bool visual_stimuli, bool auditory_stimuli, bool tactile_stimuli){
    if (visual_stimuli == HIGH){
        digitalWrite(visual_stimulus_led_sx, stimulus_sx);
        digitalWrite(visual_stimulus_led_dx, stimulus_dx);
        //Serial.println("Produce visual stimuli");
    }
    if (auditory_stimuli == HIGH){
        if (stimulus_sx == HIGH){
            Serial.println("Produce auditory sx stimulus");
        }
        if (stimulus_sx == HIGH){
            Serial.println("Produce auditory dx stimulus");
        }
    }
    if (tactile_stimuli == HIGH){
        digitalWrite(tactile_stimulus_actuator_sx, stimulus_sx);
        digitalWrite(tactile_stimulus_actuator_dx, stimulus_dx);
        //Serial.println("Produce tactile stimuli");
    }  
}

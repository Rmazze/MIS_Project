void produce_stimuli(bool stimulus_sx, bool stimulus_dx, bool visual_stimuli, bool auditory_stimuli, bool tactile_stimuli){
    if (visual_stimuli == HIGH){
        digitalWrite(visual_stimulus_led_sx, stimulus_sx);
        digitalWrite(visual_stimulus_led_dx, stimulus_dx);
        //Serial.println("Produce visual stimuli");
    }
    if (auditory_stimuli == HIGH){
        //send serial message to activate sound for sx
        //send serial message to activate sound for dx
        //Serial.println("Produce auditory stimuli");
    }
    if (tactile_stimuli == HIGH){
        digitalWrite(tactile_stimulus_actuator_sx, stimulus_sx);
        digitalWrite(tactile_stimulus_actuator_dx, stimulus_dx);
        //Serial.println("Produce tactile stimuli");
    }  
}

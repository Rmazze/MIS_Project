void select_stimuli(int stimuli_type, bool &visual_stimuli, bool &auditory_stimuli, bool &tactile_stimuli){
    switch(stimuli_type){
        case(0): visual_stimuli = HIGH;
                 auditory_stimuli = LOW;  
                 tactile_stimuli = LOW;
                 Serial.println("Visual stimuli");
                 break;
        case(1): visual_stimuli = LOW;
                 auditory_stimuli = HIGH;  
                 tactile_stimuli = LOW;
                 Serial.println("Auditory stimuli");
                 break;
        case(2): visual_stimuli = LOW;
                 auditory_stimuli = LOW;  
                 tactile_stimuli = HIGH;
                 Serial.println("Tactile stimuli");
                 break;
        case(3): visual_stimuli = HIGH;
                 auditory_stimuli = HIGH;  
                 tactile_stimuli = LOW;
                 Serial.println("Visual and auditory stimuli");
                 break;
        case(4): visual_stimuli = HIGH;
                 auditory_stimuli = LOW;  
                 tactile_stimuli = HIGH;
                 Serial.println("Visual and tactile stimuli");
                 break;
        case(5): visual_stimuli = LOW;
                 auditory_stimuli = HIGH;  
                 tactile_stimuli = HIGH;
                 Serial.println("Auditory and tactile stimuli");
                 break;
        case(6): visual_stimuli = HIGH;
                 auditory_stimuli = HIGH;  
                 tactile_stimuli = HIGH;
                 Serial.println("All stimuli");
                 break;
        default: visual_stimuli = LOW;
                 auditory_stimuli = LOW;  
                 tactile_stimuli = LOW;
                 Serial.println("No stimuli");
    }
}

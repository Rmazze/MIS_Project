void select_stimuli_regex(char received_buffer[], bool &visual_stimuli, bool &auditory_stimuli, bool &tactile_stimuli){  
    if (received_buffer[1] == 'V' || received_buffer[3] == 'V'){
        visual_stimuli = HIGH;
    } else{
        visual_stimuli = LOW;    
    }

    if (received_buffer[3] == 'A'){
        auditory_stimuli = HIGH;
    } else{
        auditory_stimuli = LOW;    
    }

    if (received_buffer[5] == 'T'|| received_buffer[3] == 'T'){
        tactile_stimuli = HIGH;
    } else{
        tactile_stimuli = LOW;    
    } 

    Serial.println("Selected stimuli," + String(visual_stimuli) + "," + String(auditory_stimuli) + "," + String(tactile_stimuli));
}

//parse the received chars from the serial COM and activate the required signals
void select_stimuli_char(char receivedChars_test[], bool &visual_stimuli, bool &auditory_stimuli, bool &tactile_stimuli){
    char * strtokIndx; // this is used by strtok() as an index
    char visual_stimuli_char[2];
    char auditory_stimuli_char[2];
    char tactile_stimuli_char[2];
    
    strtokIndx = strtok(receivedChars_test,",");      // get the first part - the string
    strcpy(visual_stimuli_char, strtokIndx);
    strtokIndx = strtok(NULL,",");      // this continues where the previous call left off
    strcpy(auditory_stimuli_char, strtokIndx);
    strtokIndx = strtok(NULL,",");      // this continues where the previous call left off
    strcpy(tactile_stimuli_char, strtokIndx);
    
    if (visual_stimuli_char[0] == 'V'){
        visual_stimuli = HIGH;
    } else{
        visual_stimuli = LOW;    
    }

    if (auditory_stimuli_char[0] == 'A'){
        auditory_stimuli = HIGH;
    } else{
        auditory_stimuli = LOW;    
    }

    if (tactile_stimuli_char[0] == 'T'){
        tactile_stimuli = HIGH;
    } else{
        tactile_stimuli = LOW;    
    } 
}
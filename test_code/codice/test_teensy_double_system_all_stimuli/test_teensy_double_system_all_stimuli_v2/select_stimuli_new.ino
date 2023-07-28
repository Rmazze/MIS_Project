//parse the received chars from the serial COM and activate the required signals
//void select_stimuli_char(char receivedChars_test[], bool &visual_stimuli, bool &auditory_stimuli, bool &tactile_stimuli){
//    char * strtokIndx; // this is used by strtok() as an index
//    char visual_stimuli_char[2];
//    char auditory_stimuli_char[2];
//    char tactile_stimuli_char[2];
//    
//    strtokIndx = strtok(receivedChars_test,",");      // get the first part - the string
//    strcpy(visual_stimuli_char, strtokIndx);
//    strtokIndx = strtok(NULL,",");      // this continues where the previous call left off
//    strcpy(auditory_stimuli_char, strtokIndx);
//    strtokIndx = strtok(NULL,",");      // this continues where the previous call left off
//    strcpy(tactile_stimuli_char, strtokIndx);
//    
//    if (visual_stimuli_char[0] == 'V'){
//        visual_stimuli = HIGH;
//    } else{
//        visual_stimuli = LOW;    
//    }
//
//    if (auditory_stimuli_char[0] == 'A'){
//        auditory_stimuli = HIGH;
//    } else{
//        auditory_stimuli = LOW;    
//    }
//
//    if (tactile_stimuli_char[0] == 'T'){
//        tactile_stimuli = HIGH;
//    } else{
//        tactile_stimuli = LOW;    
//    } 
//
//    //Serial.print("visual_stimuli: " + String(visual_stimuli));
//    //Serial.print(" auditory_stimuli: " + String(auditory_stimuli));
//    //Serial.println(" tactile_stimuli: " + String(tactile_stimuli));
//    Serial.println("Selected stimuli," + String(visual_stimuli) + "," + String(auditory_stimuli) + "," + String(tactile_stimuli));
//}


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

    //Serial.print("visual_stimuli: " + String(visual_stimuli));
    //Serial.print(" auditory_stimuli: " + String(auditory_stimuli));
    //Serial.println(" tactile_stimuli: " + String(tactile_stimuli));
    Serial.println("Selected stimuli," + String(visual_stimuli) + "," + String(auditory_stimuli) + "," + String(tactile_stimuli));
}

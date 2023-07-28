void reset_from_server(char receivedChars_reset[], int &program_execution_state){    
    if (receivedChars_reset[0] == 'R'){
        program_execution_state = -1;
    } 
}


void parseCom ( char commands[]){
  if((commands[1] == 'V' || commands[1] == 'v') && (commands[3] == 'A'|| commands[3] == 'a') && (commands[5] == 'T'|| commands[5] == 't')){
    //Serial.println("looloA");

    if(!statecom){
      //commandSerial = commands;
      strcpy(commandSerial, commands);
    }
    
    statecom = true;
    stateSerial = true;
  }
  else if(commands[0] == 'R'){
    Serial.println("B");
    statecom = true;
  }
  else{
    Serial.println("E");
    statecom = false;
  }
}

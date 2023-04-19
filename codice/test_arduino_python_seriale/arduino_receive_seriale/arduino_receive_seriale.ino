// variables for the serial communication
//how many characters to wait
const byte numChars_test = 4; // 1 for stimulus (3) +1 for termination character
const byte numChars_reset = 2; // one for reset signal +1 for termination character

// receive a string containing start and end marker and letters separated by a comma e.g. <v,A,T>
// here we store only the letters, if a letter is uppercase means we want to activate that stimulus
char receivedChars_test[numChars_test];
// receive a string containing start and end marker and a letter "R"
// here we store only the letters, if we receive 'R' it means we want to reset the execution state
char receivedChars_reset[numChars_reset];

//idicate that a new massage has been received
boolean newData_test = false;
boolean newData_reset = false;

// markers for messages regarding stimuli selection
char startMarker_test = '<';
char endMarker_test = '>';
//markers regarding reset signal
char startMarker_reset = '"';
char endMarker_reset = '"';

void setup() {
  Serial.begin(115200);
}

void loop() {
  recvWithStartEndMarkers(receivedChars_test, numChars_test, newData_test, startMarker_test, endMarker_test);
  showNewData(receivedChars_test, newData_test);
  recvWithStartEndMarkers(receivedChars_reset, numChars_reset, newData_reset, startMarker_reset, endMarker_reset);
  showNewData(receivedChars_reset, newData_reset);
} 

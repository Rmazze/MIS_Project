
void recvWithStartEndMarkers(char receivedChars[], byte numChars, boolean &newData, char startMarker, char endMarker) {
    static bool recvInProgress = false;
    static byte ndx = 0;
    
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//just for debug purposes
void showNewData(char receivedChars[], boolean &newData) {
    if (newData == true) {
        Serial.print("This just in ... ");
        Serial.println(receivedChars);
        newData = false;
    }
}


//void parseData() {
//
//    // split the data into its parts
//    
//  char * strtokIndx; // this is used by strtok() as an index
//  
//  strtokIndx = strtok(receivedChars,",");      // get the first part - the string
//  strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC
//  
//  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
//  integerFromPC = atoi(strtokIndx);     // convert this part to an integer
//  
//  strtokIndx = strtok(NULL, ","); 
//  floatFromPC = atof(strtokIndx);     // convert this part to a float
//
//}

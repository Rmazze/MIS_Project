// Serial test script
#define ready_led 26

bool ready_led_state = LOW;

int setPoint = 55;
String readedString;

void setup()
{

  Serial.begin(115200);  // initialize serial communications at 9600 bps
  pinMode(ready_led, OUTPUT);
  
}

void loop()
{
 // serial read section
  while (Serial.available()) // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
  {
    delay(30);  //delay to allow buffer to fill 
    if (Serial.available() >0)
    {
      readedString = Serial.readStringUntil('\n');
      //char c = Serial.read();  //gets one byte from serial buffer
      //readedString += c; //makes the string readString
    }
  }

  int str_len = readedString.length() + 1; 
  char readedString_char[str_len];
  readedString.toCharArray(readedString_char, str_len);

  delay(500);
  if (readedString_char[0] == '<'){
        ready_led_state = HIGH;
        Serial.println("First char <");
        //if (readedString_char[1] == 'V'){
        //  Serial.println("second char V");
        //}
  } else{
        Serial.println("First char: " + readedString_char[0]);    
  }
  digitalWrite(ready_led, ready_led_state);
  // serial write section

  //Serial.println(readedString);
  Serial.flush();
}

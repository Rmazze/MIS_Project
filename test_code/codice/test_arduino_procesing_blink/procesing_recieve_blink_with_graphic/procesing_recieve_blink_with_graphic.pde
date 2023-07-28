import processing.serial.*;


Serial myPort;  // Create object from Serial class
String val;     // Data received from the serial port
String last_val;

void setup(){
  // I know that the first port in the serial list on my mac
  // is Serial.list()[0].
  // On Windows machines, this generally opens COM1.
  // Open whatever port is the one you're using.
  //String portName = Serial.list()[0]; //change the 0 to a 1 or 2 etc. to match your port
  //myPort = new Serial(this, portName, 115200);
  myPort = new Serial(this, "COM3", 115200);
  size(1080, 750);

}

void draw()
{
  background(0);
  fill(255); //text white
  PFont f = createFont("Georgia", 70);
  textFont(f);
  textSize(32);
  text("recieved Value: ", 10, 64);
  fill(255,0,0);
  textSize(32);
  //text(val, 15, 115);
  /*if (myPort.available() > 0){  // If data is available,
    val = myPort.readStringUntil('\n');         // read it and store it in val
  }*/
  if ((val != null) && (val != last_val)){
    last_val = val;

    println(val); //print it out in the console
    text(val, 15, 115);
  }
  delay(1000);

}

void serialEvent(Serial myPort){
  val = myPort.readStringUntil('\n');
}

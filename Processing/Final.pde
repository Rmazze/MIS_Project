/*
Imports, variables declaration and object instatiation.
*/
import processing.serial.*;

int status = 0;    // status of the program
Serial port;    // port object of the Serial class
String input;    // value received from the serial port
int readVal = 0;    // integer value received from the serial port
PFont Ftimer, Fwin, Floss;    // objects of type PFont that will contain the chosen font to use for the timer, for the win and for the loss
float p = 0;    // contain the time at which the timer is paused

Timer timer;    // object of type Timer
boolean running;    // keeps whether the Timer object is running or not

int happyDur = 2880;    // duration of the happy melody
float winStart = 0;    // float value that contains the instant of time at which the win animation has started
boolean winStarted = false;    // boolean that describe whether the win animation has started or not
boolean winFinished = false;    // bolean that describe whether the win animation has finishe or not

int sadDur = 3800;    // duration of the sad melody
float lossStart = 0;    // float value that contains the instant of time at which the loss animation has started
boolean lossStarted = false;    // boolean that describe whether the loss animation has started or not
boolean lossFinished = false;    // bolean that describe whether the loss animation has finishe or not
boolean init = false;    // boolean that describe whether the loss animation has been initialized or not
float xpos1 = 0;    // position of the drop1 in the x axis
float ypos1 = 0;    // position of the drop1 in the y axis
float speed1 = 10;    // speed of the drop1 in the y axis
float xpos2 = 0;    // position of the drop2 in the x axis
float ypos2 = 0;    // position of the drop2 in the y axis
float speed2 = 10;    // speed of the drop2 in the y axis



/*
Setup function runned once at every execution of the code.
*/
void setup() {
  // Serial communication setup
  String portName = "/dev/tty.usbmodem1101";
  port = new Serial(this, portName, 9600);    // instantiate the port
  
  // Display setup
  size (700, 300);    // set the screen size and variable width = 700 pixels and height = 300 pixels
  background(0xFFFFFFFF);    // set the background color
  Ftimer = createFont("Chalkboard", 16, true);    // create the font "Chalkboard", 16 point, anti-aliasing on
  Fwin = createFont("SpaceTime-Regular", 16, true);    // create the font "SpaceTime-Regular", 16 point, anti-aliasing on
  Floss = createFont("Phosphate-Inline", 16, true);    // create the font "Phosphate-Inline", 16 point, anti-aliasing on
  noStroke();    // disable drawing the stroke
  smooth();    // draws all geometry with smooth (anti-aliased) edges
  
  // Elements setup
  timer = new Timer();    // create the Timer object
}



/*
Draw function runned repeatedly
*/
void draw() {
  // Handling of the states of the program. The program has four states:
  // 0: initial state of the progam. Here a communication on the serial port is waited
  //    and once it comes the program is diverted on a different state accord with the received signal.
  // 1: the timer is started.
  // 2: the win animation is executed.
  // 3: the loss animation is executed.
  switch(status) {
    case 0: if (port.available() > 0) {    // listen on the serial port for communication from Arduino
                input = port.readStringUntil('\n');    // read a value front the serial port
                try {
                    readVal = Integer.valueOf(input.trim());
                    
                    if (readVal == 0) {
                      status = 1;
                    }
                    else if (readVal == 1) {
                      status = 2;
                    }
                    else if (readVal == 2) {
                      status = 3;
                    }
                    else {
                      println("Unknown serial input");
                    }
                }
                catch(Exception e) {
                  ;
                }
      
            }
            break;
            
    case 1: timer.display(Ftimer);
            if (running == false) {
              timer.start();
            }
            
            if (port.available() > 0) {    // listen on the serial port for communication from Arduino
                input = port.readStringUntil('\n');    // read a value front the serial port
                try {
                    readVal = Integer.valueOf(input.trim());
                    
                    if (readVal == 1) {
                      status = 2;
                    }
                    else if (readVal == 2) {
                      status = 3;
                    }
                }
                catch(Exception e) {
                  ;
                }
      
            }
            break;
            
    case 2: if (winStarted == false) {
               p = timer.pause();
               background(0xFFFFFFFF);
               winStart = millis();
               winStarted = true;
               HappyConfetti(winStart, p);
             }
             else if (winFinished == false) {
               HappyConfetti(winStart, p);
             }
             else {
               status = 0;
               winStarted = false;
               winFinished = false;
             }
             break;
            
    case 3: if (lossStarted == false) {
               p = timer.pause();
               background(0xFFFFFFFF);
               lossStart = millis();
               lossStarted = true;
               SadRain(lossStart);
             }
             else if (lossFinished == false) {
               SadRain(lossStart);
             }
             else {
               status = 0;
               lossStarted = false;
               lossFinished = false;
               init = false;
             }
             break;
  }
}



/*
Class Timer.
It allows to create a timer object and use it.
*/
class Timer {
  /*
  Variable declaration.
  */
  long startTime; // time in ms at which the timer has started
  long runnedTime; // hold the total time runned so far
  String time; // string to output the time on the screen
  
  /*
  Constructor.
  */
  Timer() {
    running = false;
    runnedTime = 0;
    startTime = 0;
  }
  
  /*
  Method that starts the timer.
  */
  void start() {
    running = true;
    startTime = millis(); // milliseconds since the applet has started
  }
  
  /*
  Method that restarts the timer.
  */
  void restart() {
    start();
  }
  
  /*
  Method that pauses the timer.
  */
  float pause() {
    if (running) {
      runnedTime = millis() - startTime;
      running = false;
      return runnedTime;
    }
    else {
      return 0.0;
    }
  }
  
  /*
  Method that resume the timer after it has been paused.
  */
  void resume() {
    if (!running) {
      startTime = millis() - runnedTime; // startTime is set to runnedTime milliseconds before the current time
      running = true;
    }
  }
  
  /*
  Method that returns the time passed since the starting of the timer.
  If the Timer object have been paused it returns the time at which it has been stopped.
  */
  float currentTime() {
    if (running) {
      // The time passed since the starting of the timer is computed as the subraction
      // between the milliseconds since the applet has started (millis())
      // and the milliseconds since the Timer has started.
      return ((millis() - startTime)/1000.0); 
    }
    else {
      return (runnedTime/1000.0);
    }
  }
  
  /*
  Method that display the current value of the Timer.
  */
  void display(PFont f) {
    textFont(f, 50); // specify the font to use
    fill(123, 125, 125); // specify the font color
    
    // Print 0.0000 at the beginning until the timer is not started
    if (startTime == 0) {
      time = str(startTime)+"00";
      text(time, width/2-60, height/2+10);
    }
    else {
      background(0xFFFFFFFF);
      time = str(currentTime());
      text(time, width/2-60, height/2+10);
    }
  }
}



/*
Function that creates the drop shape.

:param d: drop shape composed of a triangle on a circle
:param head: triangle of the drop
:param body: circle of the drop
*/
PShape defineDrop(int col) {
  PShape d, head, body;
  
  // Create the shape group
  d = createShape(GROUP);
  
  // Make two shapes
  head = createShape(TRIANGLE, width/2, 0, width/2-10, 10,  width/2+10, 10);
  head.setFill(col);
  head.setStroke(col);
  body = createShape(ELLIPSE, width/2, 13, 20, 21);
  body.setFill(col);
  body.setStroke(col);
  
  // Add the two shapes to the group
  d.addChild(body);
  d.addChild(head);
  
  return d;
}



/*
Function HappyConfetti.
It allows to create the animation for when the user is able to catch the balls.

:param start: start time of the animation
:param t: time at which the user catched the balls

:var colors: list of colors for the the confetti
:var n: integer that will contain the color of one confetti
:var size: integer that will contain the diameter of one confetti
:var time: string for the display of the total time of the timer
*/
void HappyConfetti(float start, float t) {
  int[] colors = {0xFFCFFF00, 0xFF00CFFF, 0xFFFF00CF, 0xFFFFFF00, 0xFFFF5C4D};
  int n = 0;
  int size = 0;
  String time;
  
  // Drawing of confetti for the entire duration of the melody
  if ((millis() - start) < happyDur) {
    // Opaque background creation
    fill(0xFFFFFFFF, 10);    // set the color used to fill shapes. Here the opacity is set to 10
    rect(0, 0, width, height);    // draw a rectangle of the same size of the window
    
    // Confetti creation
    n = int(random(0, colors.length));    // choose the color of a confetti
    fill(colors[n]);
    size = int(random(20, 50));    // choose the size of a confetti
    ellipse(random(width), random(height), size, size);    // draw a confetti
  }
  else {
    // Drawing of the congratulation text
    
    // Opaque background creation
    fill(0xFFFFFFFF, 200);    // set the color used to fill shapes. Here the opacity is set to 10
    rect(0, 0, width, height);    // draw a rectangle of the same size of the window
    
    // Print the text
    textFont(Fwin, 100);
    fill(0xFF1DE239);
    text("Good Job!", width/2-300, height/2+10);
    
    // Print of the total time
    fill(0xFFFFFFFF);
    rectMode(CORNER);
    rect(width/3*2, height-50, width/3, 50);
    textFont(Ftimer, 20);
    fill(123, 125, 125);
    time = "Total time: " + str(t/1000);
    text(time, (width/3*2)+20, height-20);
    winFinished = true;
  }
}



/*
Function SadRain.
It allows to create the animation for when the user is not able to catch the balls.

:param start: start time of the animation

:var drop1: the PShape object that will be a drop
:var drop2: the PShape object that will be a drop
:var colors: list of colors for the the drops
:var n1: integer that will contain the color of drop1
:var n2: integer that will contain the color of drop2
*/
void SadRain(float start) {
  PShape drop1, drop2;
  int[] colors = {0xFF6AABD2, 0xFF385E72, 0xFF646FDE, 0xFF6896E8, 0xFF68D9E8, 0xFF64DECB};
  int n1 = 0, n2 = 0;
  
  // Initialization of the animation
  if (init == false) {
    xpos1 = random(-width/2+100, width/2-100);    // randomly initialize the position of the drop1 in the x axis
  
    // Initialize the position of the drop2 in the x axis according to drop1's position
    if (xpos1 > 0) {
      xpos2 = xpos1 + 200;
    }
    else {
      xpos2 = xpos1 - 200;
    }
    
    n1 = int(random(0, colors.length));    // initialize the color of drop1
    n2 = int(random(0, colors.length));    // initialize the color of drop2
    
    init = true;
  }
  
  else {
    if ((millis() - start) < sadDur) {
      // Background creation
      fill(0xFFFFFFFF);
      rect(0, 0, width, height);
      
      
      // Instantiate drop1
      drop1 = defineDrop(colors[n1]);    // define the drop shape
      ypos1 = ypos1 + speed1;    // initialize the position in the y axis according to the speed
      shape(drop1, xpos1, ypos1);    // create the shape
      
      // Control the position in the y axis of drop1. Once the bottom is reached restart the drop from the top of the screen
      if (ypos1 > height){
        xpos1 = random(-width/2+100, width/2-100);     // randomly initialize the position of the drop1 in the x axis
        //speed1 = random(5, 10);    // randomly choose the speed
        speed1 = 10;
        ypos1 = 0;    // reset the position of drop1 in the y axis
        n1 = int(random(0, colors.length));    // set the color of drop1
      }
      
      
      // Instantiate drop2
      drop2 = defineDrop(colors[n2]);    // define the drop shape
      ypos2 += speed2;    // initialize the position in the y axis according to the speed
      shape(drop2, xpos2, ypos2);    // create the shape
      
      // Control the position in the y axis of drop2. Once the bottom is reached restart the drop from the top of the screen
      if (ypos2 > height){
        // Initialize the position of the drop2 in the x axis according to drop1's position
        if (xpos1 > 0) {
          xpos2 = xpos1 + 200;
        }
        else {
          xpos2 = xpos1 - 200;
        }
        
        //speed2 = random(5, 10);    // randomly choose the speed
        speed2 = 8;
        ypos2 = 0;    // reset the position of drop2 in the y axis
        n2 = int(random(0, colors.length));    // set the color of drop2
      }
    }
    else {
      // Drawing of the "Try again" text
      
      // Opaque background creation
      fill(0xFFFFFFFF, 90);
      rect(0, 0, width, height);
      
      // Print the text
      textFont(Floss, 100);
      fill(0xFFEC264B);
      text("Try again", width/2-230, height/2+25);
      lossFinished = true;
    }
  }
}

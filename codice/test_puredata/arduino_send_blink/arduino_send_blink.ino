#define x

int x_state = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  delay(10000);
  if (x_state == 0){
  x_state = 1;
  }
  else if (x_state == 1){x_state = 2;
  }
  else {x_state = 0;
  }
  Serial.print("x_state, ");
  Serial.println(x_state);
}

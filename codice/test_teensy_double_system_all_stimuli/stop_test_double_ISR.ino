void stop_test_ISR_sx(){
  test_time_end_sx = millis();
  ongoing_test_sx = LOW;
}

void stop_test_ISR_dx(){
  test_time_end_dx = millis();
  ongoing_test_dx = LOW;
}

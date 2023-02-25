void stop_test_ISR() {
  test_time_end = millis();
  visual_stimulus_led_state = LOW;
  led_start_state = LOW;
  led_stop_state = HIGH;
  program_execution_state = 4;
}

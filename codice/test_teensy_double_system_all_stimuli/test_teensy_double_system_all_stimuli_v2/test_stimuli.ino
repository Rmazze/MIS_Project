void test_dimuli(unsigned long stimuly_duration){
    //produce visual stimuli
    digitalWrite(visual_stimulus_led_sx, HIGH);
    delay(stimuly_duration);
    digitalWrite(visual_stimulus_led_sx, LOW);
    delay(stimuly_duration + 1000);

    digitalWrite(visual_stimulus_led_dx, HIGH);
    delay(stimuly_duration);
    digitalWrite(visual_stimulus_led_dx, LOW);
    delay(stimuly_duration + 1000);

    digitalWrite(visual_stimulus_led_sx, HIGH);
    digitalWrite(visual_stimulus_led_dx, HIGH);
    delay(stimuly_duration);
    digitalWrite(visual_stimulus_led_sx, LOW);
    digitalWrite(visual_stimulus_led_dx, LOW);
    delay(stimuly_duration + 1000);

    //produce tactile stimuli
    digitalWrite(tactile_stimulus_actuator_sx, HIGH);
    delay(stimuly_duration);
    digitalWrite(tactile_stimulus_actuator_sx, LOW);
    delay(stimuly_duration + 1000);

    digitalWrite(tactile_stimulus_actuator_dx, HIGH);
    delay(stimuly_duration);
    digitalWrite(tactile_stimulus_actuator_dx, LOW);
    delay(stimuly_duration + 1000);

    digitalWrite(tactile_stimulus_actuator_sx, HIGH);
    digitalWrite(tactile_stimulus_actuator_dx, HIGH);
    delay(stimuly_duration);
    digitalWrite(tactile_stimulus_actuator_sx, LOW);
    digitalWrite(tactile_stimulus_actuator_dx, LOW);
    delay(stimuly_duration + 1000);

    //produce auditori stimuli //ma abbiamo diversi stimoli per la pallina dx o sx?
    Serial.println("AUDSX");// command to invoke left audio source
    delay(stimuly_duration + 1000);

    Serial.println("AUDDX");// command to invoke right audio source
    delay(stimuly_duration + 1000);

    Serial.println("AUDXX"); // command to invoke both audio sources
    delay(stimuly_duration + 1000);
}

void test_visual_stimuli(unsigned long stimuly_duration){
    digitalWrite(visual_stimulus_led_sx, HIGH);
    delay(stimuly_duration);
    digitalWrite(visual_stimulus_led_sx, LOW);
    delay(stimuly_duration + 1000);

    digitalWrite(visual_stimulus_led_dx, HIGH);
    delay(stimuly_duration);
    digitalWrite(visual_stimulus_led_dx, LOW);
    delay(stimuly_duration + 1000);

    digitalWrite(visual_stimulus_led_sx, HIGH);
    digitalWrite(visual_stimulus_led_dx, HIGH);
    delay(stimuly_duration);
    digitalWrite(visual_stimulus_led_sx, LOW);
    digitalWrite(visual_stimulus_led_dx, LOW);
    delay(stimuly_duration + 1000);
}

void test_tactile_stimuli(unsigned long stimuly_duration){
    digitalWrite(tactile_stimulus_actuator_sx, HIGH);
    delay(stimuly_duration);
    digitalWrite(tactile_stimulus_actuator_sx, LOW);
    delay(stimuly_duration + 1000);

    digitalWrite(tactile_stimulus_actuator_dx, HIGH);
    delay(stimuly_duration);
    digitalWrite(tactile_stimulus_actuator_dx, LOW);
    delay(stimuly_duration + 1000);

    digitalWrite(tactile_stimulus_actuator_sx, HIGH);
    digitalWrite(tactile_stimulus_actuator_dx, HIGH);
    delay(stimuly_duration);
    digitalWrite(tactile_stimulus_actuator_sx, LOW);
    digitalWrite(tactile_stimulus_actuator_dx, LOW);
    delay(stimuly_duration + 1000);
}

void test_audio_stimuli(unsigned long stimuly_duration){
    Serial.println("AUDSX");// command to invoke left audio source
    delay(stimuly_duration + 1000);

    Serial.println("AUDDX");// command to invoke right audio source
    delay(stimuly_duration + 1000);

    Serial.println("AUDXX"); // command to invoke both audio sources
    delay(stimuly_duration + 1000);
}

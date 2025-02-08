#include <USB.h>
#include <USBHIDKeyboard.h>

USBHIDKeyboard keyboard;


void setup() {
  Serial.begin(9600);
  keyboard.begin(KeyboardLayout_fr_FR);
  USB.begin();
}

void loop() {
  if (Serial.available() != 0) {
    String data = Serial.readStringUntil('\n');
    
    Serial.print("recu : ");
    Serial.println(data);

    keyboard.print(data);
    keyboard.press(KEY_RETURN);
    delay(100);
    keyboard.release(KEY_RETURN);
  }
}
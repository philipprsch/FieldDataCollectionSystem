#include "helpers.h"

#include "defines.h"

#include "Debugger.h"
#include "Brain.h"

#include <avr/wdt.h>



String inputString = "";      // A string to hold incoming data
bool stringComplete = false;  // Whether the string is complete 

#define ONBOARD_LED 13

Brain brain = Brain();
void setup() {
  Serial.begin(9600);
  //wdt_enable(WDTO_2S);
  //wdt_disable();
  //inputString.reserve(50);
  Debugger::init();
  pinMode(ONBOARD_LED, OUTPUT);
  for (char i = 0; i < 3; i++) {
    digitalWrite(ONBOARD_LED, HIGH);
    delay(100);
    digitalWrite(ONBOARD_LED, LOW);
    delay(100);
  }
  DEBUG_PRINTLN("A reset occured!");
  
  DEBUG_PRINT("Memory: ");
  DEBUG_PRINTLN(freeMemory());
  

  //brain.handleInput("/setup 21,21-0,2");
}



void loop() {

  // while (Serial.available() == 0) {}     //wait for data available
  // String inputString = Serial.readString();  //read until timeout
  // //inputString.trim();
  // stringComplete = true;

  if (stringComplete) {
    //inputString.trim();
    brain.handleInput(inputString);
    inputString = "";

    stringComplete = false;
  }
  
  //   while (Serial.available() > 0) {
  //   char inChar = (char)Serial.read();  // Read the next byte

  //   // If the incoming character is a newline, set stringComplete flag
  //   if (inChar == '\n') {
  //     stringComplete = true;
  //   } else {
  //     inputString.concat(inChar);  // Append character to the input string
  //   }
  // }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();  // Read the next byte

    // If the incoming character is a newline, set stringComplete flag
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString.concat(inChar);  // Append character to the input string
    }
  }
  //delay(8); //Testing
}
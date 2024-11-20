#include "helpers.h"

#include "defines.h"

#include "Debugger.h"
#include "Brain.h"

#include <avr/wdt.h>

#define ONBOARD_LED 13

#define SERIAL_INPUT_BUFFER_SIZE 50

char inputBuffer[SERIAL_INPUT_BUFFER_SIZE];      // A string to hold incoming data
int bufferIndex = 0;
//bool stringComplete = false;  // Whether the string is complete 

void setup() {
  Serial.begin(9600);
  //wdt_enable(WDTO_2S);
  //wdt_disable();
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
}

Brain brain = Brain();

void loop() {
    while (Serial.available() > 0) {      // Check if data is available
        char receivedChar = Serial.read(); // Read a character

        if (receivedChar == '\n') {       // Check for newline (end of input)
            inputBuffer[bufferIndex] = '\0';    // Null-terminate the string
            DEBUG_PRINTLN("You entered: ");
            DEBUG_PRINTLN(inputBuffer);  // Print the entered string
            brain.handleInput(inputBuffer);
            bufferIndex = 0;                    // Reset buffer index for the next input
        } else if (bufferIndex < SERIAL_INPUT_BUFFER_SIZE - 1) { 
            // Only add the character if there is space
            inputBuffer[bufferIndex++] = receivedChar;
        } else {
            DEBUG_PRINTLN("Buffer overflow! Input too long.");
            brain.sendError(ERR_INPUT_BUFFER_OVERFLOW);
            bufferIndex = 0; // Reset buffer to handle new input
        }
    }

  // if (stringComplete) {
  //   brain.handleInput(inputString);
  //   inputString = "";
  //   stringComplete = false;
  // }

}



// void serialEvent() {
//   while (Serial.available()) {
//     char inChar = (char)Serial.read();  // Read the next byte

//     // If the incoming character is a newline, set stringComplete flag
//     if (inChar == '\n') {
//       stringComplete = true;
//     } else {
//       inputString += inChar;  // Append character to the input string
//     }
//   }
//   //delay(8); //Testing
// }
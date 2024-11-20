#pragma once
#include "defines.h"

class Debugger {
 private:
  static String logs;

 public:
  Debugger() {}

  static void init() {
    logs = "";
    logs.reserve(60);
  }
  static void log(const String str) { 
    DEBUG_PRINTLN("Logging to Debugger: " + str);
    logs = logs + String(millis()) + ": " + str + '\n'; 
    DEBUG_PRINTLN(logs);
    }
  static void clear() { logs = ""; }
  static void print() {
    int length = logs.length();
    int offset = 0;

    while (offset < length) {
      // Determine the size of the next chunk
      int chunkSize = min(SERIAL_TX_BUFFER_SIZE, length - offset);

      // Extract the substring chunk
      String chunk = logs.substring(offset, offset + chunkSize);

      // Send the chunk over Serial
      Serial.print(chunk);

      // Update the offset to the next chunk
      offset += chunkSize;

      // Optional: Add a small delay to avoid overloading the Serial buffer
      delay(10);
    }
    Serial.println();
  }
};

String Debugger::logs = "";
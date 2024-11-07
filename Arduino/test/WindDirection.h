#include "LoggingDevice.h"
#include <Array.h>
#pragma once

class WindDirection : public LoggingDevice {
 private:
  char pins[8];

 public:
  WindDirection(String id, String alias, char pins[8]) : LoggingDevice(id, alias) {
     Serial.println("--Printing Pins--");
     for (char i = 0; i < 8; i++) {
      this->pins[i] = pins[i];
       Serial.print((int)pins[i]);
       Serial.print(", ");
     }
     Serial.println();
     
     Serial.println("WindDirection creation complete.");
  }
  void handleInterrupt() override {
    return;
  } //Supress error

  bool init() {
    Serial.println("Initializing WindDirection...");
    for (int i = 0; i < sizeof(this->pins)/sizeof(char); i++) {
      if ((int)this->pins[i] == 0) {
        Serial.println("Pin "+ String(i) + " is zero.");
        return false;
      }
      pinMode((int)this->pins[i], INPUT_PULLUP);
    }
    Serial.println("WindDirection initialization complete.");
    return true;
  }
  Array<bool, 8> measure() { //One possible implementation (alt. return wind direction as 2-char string)

    Array<bool, 8> result;
    for (char i = 0; i < 8; i++) {
      result[i] = (digitalRead(this->pins[i]) == HIGH); 
    }
    
    return result;
  }
  void log() override { 
    Array<bool, 8> windDirectionBool = measure();
    String result = "";
        for (int i = 0; i < 8; i++) {
        result += windDirectionBool[i] ? "1" : "0";
        if (i != 7) {
            result += ",";
        }
    }
    logParent(result); 
  }
  void handle() override {
    return;
  }
};


#pragma once

#include "LoggingDevice.h"
#include <Array.h>


class WindDirection : public LoggingDevice { //ID: 20
 private:
  char pins[8];

 public:
  WindDirection(String id, String alias, char pins[8]) : LoggingDevice(id, alias) {
     DEBUG_PRINTLN("--Printing Pins--");
     for (char i = 0; i < 8; i++) {
      this->pins[i] = pins[i];
     }
     
     DEBUG_PRINTLN("WindDirection creation complete.");
  }
  //Static public factory meethod, for creation beased on parameters
  static LoggingDevice* factory(const String params[]) {
    char pins[8];
    for (char i = 0; i < 8; i++) {
      pins[i] = (params[i + 2].toInt());
    }
    DEBUG_PRINTLN("Creating WindDiretion Object");
    return new WindDirection(params[0], params[1], pins);
  }


  void handleInterrupt() override {
    return;
  } //Supress virtual declaration error

  bool init() {
    DEBUG_PRINTLN("Initializing WindDirection...");
    for (int i = 0; i < sizeof(this->pins)/sizeof(char); i++) {
      if ((int)this->pins[i] == 0) {
        Debugger::log("Wind Direction Pin "+ String(i) + " is zero.");
        return false;
      }
      pinMode((int)this->pins[i], INPUT_PULLUP);
    }
    DEBUG_PRINTLN("WindDirection initialization complete.");
    return true;
  }
  void measure(bool mesurements[8]) { //One possible implementation (alt. return wind direction as 2-char string)

    bool result[8];
    for (char i = 0; i < 8; i++) {
      result[i] = (digitalRead(this->pins[i]) == HIGH); 
    }
  }
  void log() override { 
    bool windMeasurements[8];
    measure(windMeasurements);
    String result = "";
        for (int i = 0; i < 8; i++) {
        result += windMeasurements[i] ? "1" : "0";
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


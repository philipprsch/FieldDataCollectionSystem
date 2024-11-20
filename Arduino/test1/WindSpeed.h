#pragma once

#include "LoggingDevice.h"
#include "InterruptHandler.h"

#include "helpers.h"

class WindSpeedSensor : public LoggingDevice { //ID: 21
  private:
  int pin;

  volatile int rotationsCounter;
  long lastCounterReset;
  public:
  WindSpeedSensor(String id, String alias, int pin) : LoggingDevice(id, alias) {
    this->pin = pin;
    //this->interruptFlag = false;

    this->rotationsCounter = 0;
    this->lastCounterReset = millis();
  }
  static LoggingDevice* factory(const String params[]) {
    // DEBUG_PRINT("Memory: ");
    // DEBUG_PRINTLN(freeMemory());
    // DEBUG_PRINTLN("Factory of WindSpeed was called with params: ");
    // for (int i = 1; i < 3; i++) {
    //   DEBUG_PRINT("Param "+String(i)+": ");
    //   DEBUG_PRINT("Memory: ");
    //   DEBUG_PRINTLN(freeMemory());
    //   //if (params[i]) DEBUG_PRINT("exiists: ");
    //   //DEBUG_PRINTLN(params[i]);
    // }
    return new WindSpeedSensor("21", "21-0", 2);
    //return new WindSpeedSensor(params[0], params[1], params[2].toInt());
  }
  bool init() {
    if (this->pin == 0) return false; //Removed !this->pin for testing
    pinMode(this->pin, INPUT_PULLUP);
    DEBUG_PRINTLN("About to add interrupt for WIndSpeed");
    InterruptHandler::addInterrupt(this, &LoggingDevice::handleInterrupt, this->pin);
    DEBUG_PRINTLN("Added interrupt for WIndSpeed");
    return true;
  }
  void handleInterrupt() override {
    //this->interruptFlag = true;
    this->rotationsCounter++;
  }
  void handle() override {
    return;
  }
  void log() override {
    long now = millis();
    long delta = now - this->lastCounterReset;
    float res = (this->rotationsCounter*1000*60 / delta); //RPM
    char buffer[7];
    Debugger::log("Wind Sensor RPM: "+ String(res));

    this->lastCounterReset = now;
    this->rotationsCounter = 0;

    dtostrf(res, 4, 2, buffer);
    logParent(String(buffer));
  }
};

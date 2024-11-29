#pragma once

#include "LoggingDevice.h"
#include "InterruptHandler.h"

#include "helpers.h"

class WindSpeedSensor : public LoggingDevice { //ID: 21
  private:
  char pin;

  volatile int rotationsCounter;
  unsigned long lastCounterReset;
  public:
  WindSpeedSensor(String id, String alias, uint8_t pin) : LoggingDevice(id, alias) { //Changed to cahr
    DEBUG_PRINT("Constructor: Memory: ");
    DEBUG_PRINTLN(freeMemory());
    this->pin = pin;

    this->rotationsCounter = 0;
    this->lastCounterReset = 0; //Assigning to millis causes problems
  }
  static LoggingDevice* factory(const String params[]) {
    DEBUG_PRINT("Memory: ");
    DEBUG_PRINTLN(freeMemory());
    return new WindSpeedSensor(params[0], params[1], params[2].toInt());
  }
  bool init() {
    if (this->pin == 0) return false; //Removed !this->pin for testing
    pinMode(this->pin, INPUT_PULLUP);
    InterruptHandler::addInterrupt(this, &LoggingDevice::handleInterrupt, this->pin);
    DEBUG_PRINTLN("Added interrupt for WIndSpeed");
    return true;
  }
  void handleInterrupt() override {
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
    DEBUG_PRINTLN("Wind Sensor RPM: "+ String(res));

    this->lastCounterReset = now;
    this->rotationsCounter = 0;

    dtostrf(res, 4, 2, buffer);
    logParent(String(buffer));
  }
};

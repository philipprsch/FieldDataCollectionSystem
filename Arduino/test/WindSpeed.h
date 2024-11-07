#include "LoggingDevice.h"
#include "InterruptHandler.h"
#pragma once

class WindSpeedSensor : public LoggingDevice {
  private:
  char pin;

  volatile int rotationsCounter;
  long lastCounterReset;
  public:
  WindSpeedSensor(String id, String alias, char pin) : LoggingDevice(id, alias) {
    this->pin = pin;
    //this->interruptFlag = false;

    this->rotationsCounter = 0;
    this->lastCounterReset = millis();
  }
  bool init() {
    pinMode(this->pin, INPUT_PULLUP);
    InterruptHandler::addInterrupt(this, &LoggingDevice::handleInterrupt, 2);
    
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
    Serial.print("Wind Sensor RPM: ");
    Serial.println(res);

    this->lastCounterReset = now;
    this->rotationsCounter = 0;

    dtostrf(res, 4, 2, buffer);
    logParent(String(buffer));
  }
};

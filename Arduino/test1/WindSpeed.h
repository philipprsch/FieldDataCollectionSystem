#pragma once

#include "LoggingDevice.h"
#include "InterruptHandler.h"

#include "helpers.h"

class WindSpeedSensor : public LoggingDevice, virtual public InterruptUser { //ID: 21
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
<<<<<<< HEAD
  static LoggingDevice* factory(char** params) {
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
=======
  static LoggingDevice* factory(const String params[]) {
    DEBUG_PRINT("Memory: ");
    DEBUG_PRINTLN(freeMemory());
    return new WindSpeedSensor(params[0], params[1], params[2].toInt());
>>>>>>> 5f99b29b596e0acdcb967e2b617edae95df5405c
  }
  bool init() {
    if (this->pin == 0) return false; //Removed !this->pin for testing
    pinMode(this->pin, INPUT_PULLUP);
    noInterrupts();
    InterruptHandler::addInterrupt(this, &InterruptUser::handleInterrupt, this->pin);
    interrupts();
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

#include "LoggingDevice.h"
#include "defines.h"

class GenericDigitalInput : public LoggingDevice {
  private:
    char pin;
  public:
  GenericDigitalInput(String id, String alias, char pin) : LoggingDevice(id, alias) {
    this->pin = pin;
    DEBUG_PRINTLN("Digital input creation complete.");
  }
  static LoggingDevice* factory(const String params[]) {
    Debugger::log("Creating Generic DIgiatal Input Object");
    return new GenericDigitalInput(params[0], params[1], params[2].toInt());
  }
  bool init() {
    pinMode(this->pin, INPUT);
    return true;
  }
  void log() override {
    bool value = (digitalRead(this->pin) == HIGH);
    logParent(value? "1" : "0");
  }
  void handle() override {
    return;
  }
  void handleInterrupt() override {
    return;
  }
};


class GenericAnalogInput : public LoggingDevice {
  private:
    char pin;
  public:
  GenericAnalogInput(String id, String alias, char pin) : LoggingDevice(id, alias) {
    this->pin = analogInputToDigitalPin(pin);
    DEBUG_PRINTLN("Analog input creation complete.");
  }
  static LoggingDevice* factory(const String params[]) {
    Debugger::log("Creating Generic Analog Input Object");
    return new GenericAnalogInput(params[0], params[1], params[2].toInt());
  }
  bool init() {
    pinMode(this->pin, INPUT);
    return true;
  }
  void log() override {
    uint16_t value = analogRead(this->pin);
    logParent((String)value);
  }
  void handle() override {
    return;
  }
  void handleInterrupt() override {
    return;
  }
};

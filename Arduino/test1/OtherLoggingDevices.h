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

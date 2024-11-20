#include "defines.h"
#include "Debugger.h"
#pragma once




class LoggingDevice {
 private:

 protected:
  String id;
  String alias;

 public:
  LoggingDevice() {}
  LoggingDevice(String id, String alias) {
    this->id = id;
    this->alias = alias;

  }

  void logParent(String message) { 
    Serial.println(message);
    Debugger::log(this->alias + "logs: " + message);
    }
  virtual bool init() = 0;
  virtual void log() = 0;  // Pure virtual function
  virtual void handle() = 0;
  virtual void handleInterrupt() {
    
  }
  
  static void call(LoggingDevice* instance, void (LoggingDevice::*callback)()) {
  (instance->*callback)();
}

  String getAlias() {
    return this->alias;
  }
  String getId() {
    return this->id;
  }
};



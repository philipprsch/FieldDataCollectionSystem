
#pragma once

class LoggingDevice {
 protected:
  String id;
  String alias;

 public:
  LoggingDevice() {}
  LoggingDevice(String id, String alias) {
    this->id = id;
    this->alias = alias;
    Serial.print("LoggingDevice constructed with alias:");
    Serial.println(this->alias);

  }
  void logParent(String message) { Serial.print(message + '\n'); }
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

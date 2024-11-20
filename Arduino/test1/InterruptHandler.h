#include "LoggingDevice.h"
#pragma once

using MethodPointer = void (LoggingDevice::*)();
typedef void (*FuncPtr)();

const char MAX_INTERRUPTS = 2; //2 Interrupt pins on Arduino UNO

class InterruptHandler {
  
  static LoggingDevice* instance[MAX_INTERRUPTS];
  static MethodPointer callback[MAX_INTERRUPTS];
  
  static FuncPtr handlers[MAX_INTERRUPTS];

  static char interruptCounter;

  public:
  static void init() {
    interruptCounter = 0;
    for (int i = 0; i < MAX_INTERRUPTS; ++i) {
        instance[i] = nullptr;
        callback[i] = nullptr;
    }
    //Save all handlers manually, so they can be called when interrupt occures
    handlers[0] = &InterruptHandler::interruptHandler0;
    handlers[1] = &InterruptHandler::interruptHandler1;
  }
  static void addInterrupt(LoggingDevice *myinstance, MethodPointer mycallback, int pin, int mode = CHANGE) {
    instance[interruptCounter] = myinstance;
    callback[interruptCounter] = mycallback;
    attachInterrupt(digitalPinToInterrupt(pin), handlers[interruptCounter++], mode);
  }
  //If more Interrupt Pins are available on other board, adhust MAX_INTERRUPTS and manually add new handlers
  static void interruptHandler0() {
    (instance[0]->*callback[0])();
  }
  static void interruptHandler1() {
      (instance[1]->*callback[1])();
  }
};

LoggingDevice* InterruptHandler::instance[MAX_INTERRUPTS] = {};
MethodPointer InterruptHandler::callback[MAX_INTERRUPTS] = {};
FuncPtr InterruptHandler::handlers[MAX_INTERRUPTS] = {};
char InterruptHandler::interruptCounter = 0;

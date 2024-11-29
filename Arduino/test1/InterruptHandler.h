#include "LoggingDevice.h"
#pragma once


class InterruptUser {
  public:

  virtual void handleInterrupt() = 0;
};


using MethodPointer = void (InterruptUser::*)();
typedef void (*FuncPtr)();

#define MAX_INTERRUPTS 2 //2 Interrupt pins on Arduino UNO

class InterruptHandler {
  
  static InterruptUser* instance[MAX_INTERRUPTS];
  static MethodPointer callback[MAX_INTERRUPTS];
  
  static FuncPtr handlers[MAX_INTERRUPTS];

  static uint8_t interruptCounter;

  public:
  static void init() {
    interruptCounter = 0;
    for (uint8_t i = 0; i < MAX_INTERRUPTS; i++) {
        instance[i] = nullptr;
        callback[i] = nullptr;
    }
    //Save all handlers manually, so they can be called when interrupt occures
    handlers[0] = &InterruptHandler::interruptHandler0;
    handlers[1] = &InterruptHandler::interruptHandler1;
  }
  static void addInterrupt(InterruptUser *myinstance, MethodPointer mycallback, uint8_t pin, int mode = CHANGE) {
    
    instance[interruptCounter] = myinstance;
    callback[interruptCounter] = mycallback;
    DEBUG_PRINTLN("Adding interrupt");
    attachInterrupt(digitalPinToInterrupt(pin), handlers[interruptCounter++], mode);
    Debugger::log("Added interrupt");
  }
  //If more Interrupt Pins are available on other board, adhust MAX_INTERRUPTS and manually add new handlers
  static void interruptHandler0() {
    (instance[0]->*callback[0])();
  }
  static void interruptHandler1() {
      (instance[1]->*callback[1])();
  }
};

InterruptUser* InterruptHandler::instance[MAX_INTERRUPTS] = {};
MethodPointer InterruptHandler::callback[MAX_INTERRUPTS] = {};
FuncPtr InterruptHandler::handlers[MAX_INTERRUPTS] = {};
uint8_t InterruptHandler::interruptCounter = 0;

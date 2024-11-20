#include "helpers.h"
//#include <Array.h>
#include "LoggingDevice.h"

#include "defines.h"

//Changed include order for testing
#include "WindSpeed.h"
#include "WindDirection.h"


#include "Debugger.h"
#include <avr/wdt.h>

#pragma once

class Brain {
  private:

    struct LoggingDeviceFactoryMap {
        String deviceID;
        //LoggingDevice* (*factory)(const String params[]);
        LoggingDevice* (*factory)(const String params[]);
        char paramCount;
    };
    const LoggingDeviceFactoryMap factoryMap[SUPPORTED_DEVICES] = { //Changed order for testing
      {"21", &WindSpeedSensor::factory, 3},
      {"20", &WindDirection::factory, 10}
    };

    struct BrainMethodMap {
        String name;
        void (Brain::*func)(const String params[], char paramCount);
    };

    const BrainMethodMap commandMap[MAX_COMMANDS] = {
      {"/req", &Brain::com_req},
      {"/list", &Brain::com_list},
      {"/setup", &Brain::com_setup},
      {"/report", &Brain::com_report},
      {"/reset", &Brain::com_reset},
      {"/help", &Brain::com_help}
    };

    void com_req(const String params[], char parmCount) {
      if (!params[0]) { //Parameter 0 = Alias is not defined
        this->sendError(ERR_PARAMETER_MISSING);
        return;
      } //TODO: Check if this catches error case
      LoggingDevice* device = getDeviceByAlias(params[0]);
      if (!device) {
        this->sendError(ERR_INVALID_ALIAS);
        return;
      }
      device->log();
     }
    void com_list(const String params[], char parmCount) {
      Serial.println("Device Count: "+ String(deviceCounter));
      for (byte i = 0; i < deviceCounter; i++) {
        Serial.print("Alias: ");
        Serial.print(devices[i]->getAlias());
        Serial.print(", ID: ");
        Serial.println(devices[i]->getId());
      }
      //Alternitively: Implement infoText() Method for each Logging Device Child Class
    }
    void com_setup(const String params[], char parmCount) {
      Debugger::log("Attempting to setup device: ID = "+ params[0] + ", Alias = "+ params[1]);
      for (char i = 0; i < SUPPORTED_DEVICES; i++) {
        if (factoryMap[i].deviceID == params[0]) {
          if (getDeviceByAlias(params[1])) {
            this->sendError(ERR_ALIAS_ALREADY_EXISTS);
            return;
          }  
          if (parmCount >= factoryMap[i].paramCount) {
            DEBUG_PRINTLN("About to call facotry with params: ");
            for (int c = 0; c < parmCount; c++)
            {
              DEBUG_PRINTLN("Param "+String(c)+": " + params[c]);
            }
            
            LoggingDevice* device = factoryMap[i].factory(params);
            if (!device) {
                delete device;
                this->sendError(ERR_DEVICE_CONSTRUCTION_FAILED);
                return;
            }
            if (!device->init()) {
              this->sendError(ERR_DEVICE_INIT_FAILED);
              return;
            }
            devices[deviceCounter++] = device;
            this->sendSuccess();
            return;
          } 
          this->sendError(ERR_SETUP_PARAMETER_MISSING);
          return;
        }
      }
      this->sendError(ERR_UNSUPPORTED_DEVICE_ID);
      //Device with params[0] as ID not suppoerted
      
    }
    void com_report(const String params[], char parmCount) {
        Serial.println("---Report millis="+String(millis())+"---");
        Debugger::print();
    }
    void com_reset(const String params[], char parmCount) {
        DEBUG_PRINTLN("Resetting");
        wdt_enable(WDTO_15MS); // resets the MCU after 15 milliseconds
        while (true);
    }
    void com_help(const String params[], char parmCount) {

    }
    LoggingDevice* getDeviceByAlias(String alias) {
      for (byte i = 0; i < deviceCounter; i++) {
        if (devices[i]->getAlias() == alias) {
          return devices[i];
        }
      }
      return nullptr;  // No device found with the given alias
    }
    LoggingDevice* devices[MAX_DEVICES];
    int deviceCounter = 0;
  public:

  String myParams[MAX_PARAMETERS]; //Put here and used in constructor instead of handleInput for testing
  Brain() {
    for (char i = 0; i < MAX_PARAMETERS; i++) {
      if (!myParams[i].reserve(10)) {
        DEBUG_PRINTLN("Could not reserve space for parameter");
      }   
      myParams[i] = "abababababab";
    }
    
  }

  void sendError(int error) {
    Serial.println("!ER"+String(error)); //Commented for testing
    Debugger::log("Error: !ER"+String(error));
  }
  void sendSuccess() { 
    Serial.println("OK"); //Commented for testing
    Debugger::log("Success");
  }

  void callCommand(String name, const String params[], int paramCount) {
      for (int i = 0; i < MAX_COMMANDS; i++) {
          if (commandMap[i].name == name) {
              // Maybe Check if the number of parameters is correct for given command
              (this->*commandMap[i].func)(params, (char)paramCount);  // Call the member function, added char
              return;
          }
      }
      this->sendError(ERR_UNKNOWN_COMMAND);
  }

  void handleInput(const String &input) {
    if (input[0] != '/') {
      this->sendError(ERR_NOT_A_COMMAND);
      return; //or hanlde input ohterwise
    }
    String command, parameters;
    splitStringTwo(input, ' ', command, parameters);
    if (command != "/report") {
        Debugger::clear();
    }
    Debugger::log("Recieved: " + input);
    DEBUG_PRINTLN(command);
    DEBUG_PRINTLN(parameters);
    
    int itemCount = splitString(parameters, ',', myParams, MAX_PARAMETERS);

    callCommand(command, myParams, itemCount);
  }
};
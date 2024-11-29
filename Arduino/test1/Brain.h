#include "helpers.h"
//#include <Array.h>
#include "LoggingDevice.h"

#include "defines.h"

//Changed include order for testing
#include "WindSpeed.h"
#include "WindDirection.h"
#include "OtherLoggingDevices.h"


#include "Debugger.h"
#include <avr/wdt.h>

#pragma once

class Brain {
  private:

    struct LoggingDeviceFactoryMap {
        String deviceID;
        //LoggingDevice* (*factory)(const String params[]);
        LoggingDevice* (*factory)(char ** params);
        char paramCount;
    };
    const LoggingDeviceFactoryMap factoryMap[SUPPORTED_DEVICES] = {
      {"21", &WindSpeedSensor::factory, 3}, 
      {"20", &WindDirection::factory, 10},
      {"22", &GenericDigitalInput::factory, 3},
      {"23", &GenericAnalogInput::factory, 3}
    };

    struct BrainMethodMap {
        //char name[COMMAND_BUFFER_SIZE];
        String name;
        void (Brain::*func)(char** params, char paramCount);
    };

    #define MAX_COMMANDS 1 //Temporary

    const BrainMethodMap commandMap[MAX_COMMANDS] = {
      //{"/req", &Brain::com_req},
      //{"/list", &Brain::com_list},
      {"/setup", &Brain::com_setup} //Only test setup for now
      //{"/report", &Brain::com_report},
      //{"/reset", &Brain::com_reset},
      //{"/help", &Brain::com_help}
    };

    void com_req(const String params[], char parmCount) {
      if (params[0] == NULL) { //Parameter 0 missing = Alias is not defined
        this->sendError(ERR_PARAMETER_MISSING);
        return;
      } //TODO: Check if this catches error case
      Debugger::log("Request: Alias = "+ params[0]);
      LoggingDevice* device = getDeviceByAlias(params[0]);
      if (!device) {
        this->sendError(ERR_INVALID_ALIAS);
        return;
      }
      device->log();
     }
    void com_list(char** params, char parmCount) {
      Serial.println("Device Count: "+ String(deviceCounter));
      for (uint8_t i = 0; i < deviceCounter; i++) {
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
            DEBUG_PRINT_ARRAY(params, parmCount);
            
            LoggingDevice* device = factoryMap[i].factory(params);
            if (!device) { //Should never occure
                //delete device;
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
      this->sendError(ERR_UNSUPPORTED_DEVICE_ID); //Device with params[0] as ID not suppoerted
    }
    void com_report(char** params, char parmCount) {
        Serial.println("---Report millis="+String(millis())+"---");
        Debugger::print();
    }
    void com_reset(char** params, char parmCount) {
        DEBUG_PRINTLN("Resetting");
        wdt_enable(WDTO_15MS); // resets the MCU after 15 milliseconds
        while (true);
    }
    void com_help(const String params[], char parmCount) {
        //Not important
    }
    LoggingDevice* getDeviceByAlias(String alias) {
      for (uint8_t i = 0; i < deviceCounter; i++) {
        if (devices[i]->getAlias() == alias) {
          return devices[i];
        }
      }
      return nullptr;  // No device found with the given alias
    }
    LoggingDevice* devices[MAX_DEVICES];
    uint8_t deviceCounter = 0;
  public:

  String myParams[MAX_PARAMETERS]; //Put here and used in constructor instead of handleInput for testing
  Brain() {}

  void sendError(int error) {
    Serial.println("!ER"+String(error)); //Commented for testing
    Debugger::log("Error: !ER"+String(error));
  }
  void sendSuccess() { 
    Serial.println("OK"); //Commented for testing
    Debugger::log("Success");
  }

  void callCommand(char* name, char** params, int paramCount) {
      for (int i = 0; i < MAX_COMMANDS; i++) {
          if (commandMap[i].name == name) {
              // Maybe add check for number of parameters for given command
              (this->*commandMap[i].func)(params, (char)paramCount);  // Call the member function, added char
              return;
          }
      }
      this->sendError(ERR_UNKNOWN_COMMAND);
  }

  void handleInput(char* input) {
    if (input[0] != '/') {
      this->sendError(ERR_NOT_A_COMMAND);
      return; //or hanlde input ohterwise
    }

    char part1[PARAMETER_BUFFER_SIZE], part2[PARAMETER_BUFFER_SIZE], part3[PARAMETER_BUFFER_SIZE], part4[PARAMETER_BUFFER_SIZE];
    char part5[PARAMETER_BUFFER_SIZE], part6[PARAMETER_BUFFER_SIZE], part7[PARAMETER_BUFFER_SIZE], part8[PARAMETER_BUFFER_SIZE];
    char part9[PARAMETER_BUFFER_SIZE], part10[PARAMETER_BUFFER_SIZE];

    // Create an array of pointers to the buffers
    char* myParams[MAX_PARAMETERS] = { part1, part2, part3, part4, part5, part6, part7, part8, part9, part10 };


    char command[COMMAND_BUFFER_SIZE];
    char parameters[(PARAMETER_BUFFER_SIZE-1+1)*MAX_PARAMETERS +1];
    splitCharArrayIntoTwo(input, command, parameters, ' ');
    if (strcmp(command, "/report") != 0) {
        Debugger::clear();
    }
    Debugger::log("Recieved: " + String(input)); //For now let Debugger rely on String
    DEBUG_PRINTLN(command);
    DEBUG_PRINTLN(parameters);
    
    int itemCount = splitCharArrayIntoMultiple(parameters, myParams, MAX_PARAMETERS, ',');

    callCommand(command, myParams, itemCount);
  }
};
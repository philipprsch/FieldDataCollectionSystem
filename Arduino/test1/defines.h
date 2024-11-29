#pragma once

#define MAX_PARAMETERS 10
#define SUPPORTED_DEVICES 4 //Amount of classes / distinct devices
#define MAX_DEVICES 10
#define MAX_COMMANDS 6

//Debugging Option toggles Serial Debug messages
#define DEBUG_MODE true

#ifdef DEBUG_MODE
  #define DEBUG_PRINT(x) Serial.print(x)
  #define DEBUG_PRINTLN(x) Serial.println(x)
  #define DEBUG_PRINT_ARRAY(arr, len)        \
  for (int i = 0; i < len; i++) {   \
    Serial.print(arr[i]);           \
    if (i < len - 1) {              \
      Serial.print(", ");           \
    }                               \
  }                                 \
  Serial.println();

#else
  #define DEBUG_PRINT(x)   // Do nothing
  #define DEBUG_PRINTLN(x) // Do nothing
  #define DEBUG_PRINT_ARRAY(array, len) // Do nothing
#endif


//Error Code Definitions

#define ERR_NOT_A_COMMAND 01
//Input is not a command

#define ERR_UNKNOWN_COMMAND 02
//Input was recognized as a command, but it is invalid

#define ERR_UNSUPPORTED_DEVICE_ID 03 
//There exists no class for the provided Device ID aka. no Factory function is mapped to this ID

#define ERR_INVALID_ALIAS 04 
//Provided alias does not match any device that was previously set up

#define ERR_PARAMETER_MISSING 05
//Error due to missing / unspecified parameter (e.g. alias missing for req)

#define ERR_SETUP_PARAMETER_MISSING 06
//Same as ERR_PARAMETER_MISSING but for failed setup of Logging Device

#define ERR_DEVICE_CONSTRUCTION_FAILED 07
//Construction/Instanciation of Device Object through factory failed

#define ERR_DEVICE_INIT_FAILED 8
//Device Initialization failed

#define ERR_ALIAS_ALREADY_EXISTS 9

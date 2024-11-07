#include "helpers.h"
#include <Array.h>
#include "LoggingDevice.h"
#include "WindDirection.h"
#include "WindSpeed.h"

String inputString = "";      // A string to hold incoming data
bool stringComplete = false;  // Whether the string is complete
String command = "";

const char MAX_PARAMETERS = 10;
const char MAX_DEVICES = 10;


LoggingDevice *devices[MAX_DEVICES];
int deviceCount = 0;

//Get Logging Device Class Instance by Alias
LoggingDevice* getDeviceByAlias(String alias) {
  for (byte i = 0; i < deviceCount; i++) {
    if (devices[i]->getAlias() == alias) {
      return devices[i];
    }
  }
  return nullptr;  // No device found with the given alias
}


void setup()
{
  Serial.begin(9600);        // Start serial communication at 9600 bps
  inputString.reserve(200);  // Reserve 200 bytes for the input string

  InterruptHandler* interupthandler = new InterruptHandler();
  InterruptHandler::init();
}

void loop() {
  // Handle all devices
  for (byte i = 0; i < deviceCount; i++) {
    devices[i]->handle(); //Use -> because devices[i] is a pointer to the desired object
  }

  // Check if a complete string has been received
  if (stringComplete) {
    Serial.print("Received: ");
    Serial.println(inputString);  // Print the received string
    if (inputString[0] == '_') {  // The recieved String is a command
      command = inputString;
      Serial.println("Recieved Command: "+command);
    } else {
      if (command != "") {
        Serial.println("Executing command: "+command);
        String params[MAX_PARAMETERS];
        int itemCount = splitString(inputString, ',', params, MAX_PARAMETERS);
        Serial.println("--Printing Parameters--");
        for (char i = 0; i < itemCount; i++) {
          Serial.print(params[i]);
          Serial.print(", ");
        }
        Serial.println();     
        if (command == "_setup") {
          Serial.print("Setting up device: ");
          Serial.println(params[0]);
          // Setup based on Logging Device ID
          if (params[0] == "20") {  // 20 = Wind Direction
            Serial.println("params[0] is 20");
            char pins[8];
            for (char i = 0; i < 8; i++) {
              pins[i] = (params[i+2].toInt());
            }
            Serial.println("Creating WindDiretion Object");
            devices[deviceCount] = new WindDirection(params[0], params[1], pins);
          } else if (params[0] == "21") { //21 = Wind Speed
            Serial.println("params[0] is 21");
            devices[deviceCount] = new WindSpeedSensor(params[0], params[1], params[2].toInt());
          } else if (params[0] == "22") {  
            
          } else {
            Serial.println("Logging device ID not supported.");
            // Logging Device ID not supported by this external microcontroller
          }

          if (devices[deviceCount]) {  // Device Instance was created
            Serial.print("Initializing deviceCount=");
            Serial.println(deviceCount);
            bool iniRes = devices[deviceCount]->init();
            if (iniRes) {
              Serial.print("OK\n");
              deviceCount++;
            } else {
              Serial.print("ERROR\n"); //Could be because parameters provided after command line are bullshit
               delete devices[deviceCount];
               devices[deviceCount] = NULL;
            }      
          } else {
            Serial.println("No device instance was created.");
          }
        } else if (command == "_req") { //Main board has requested new log from sensor (with alias param[0])
          LoggingDevice* myDevice = getDeviceByAlias(params[0]);
          if (myDevice) {
            myDevice->log();
          } else { //Device not found with alias
            Serial.println("Device not found with alias: "+params[0]);
          }
          
        } else if (command == "_printDevices") {
          Serial.print("Device Count: ");
          Serial.println(deviceCount);
          for (byte i = 0; i < deviceCount; i++) {
            Serial.print("Alias: ");
            Serial.print(devices[i]->getAlias());
            Serial.print(", ID: ");
            Serial.println(devices[i]->getId());
          }
        }

        command = "";  // Reset command
      } else { //No command previiously loaded
        Serial.println("No command was previously loaded, neither is this input (ending in LF) a command");
        // No command was previously loaded, handle incoming string otherwise or
        // ignore
      }
    }

    // Clear the inputString and reset flag for the next input
    inputString = "";
    stringComplete = false;
  }
}

// SerialEvent is called whenever data is available on the serial port
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();  // Read the next byte

    // If the incoming character is a newline, set stringComplete flag
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;  // Append character to the input string
    }
  }
}

String inputString = "";      // A string to hold incoming data
bool stringComplete = false;  // Whether the string is complete
String command = "";

const int MAX_PARAMETERS = 10;
const int MAX_DEVICES = 10;

LoggingDevice* devices[MAX_DEVICES];
int deviceCount = 0;

class LoggingDevice {
public:
  void logParent(const char* message) {
    Serial.println(message+"\n");
  }
  virtual void log() = 0;  // Pure virtual function
  virtual void handle() = 0;
};

class WindDirection()
  : public LoggingDevice {
private:


public:
  WindDirection(String id, String alias, char[] pins) {
    this.pins = new char[8];
  }
  bool init() {
    for (int i = 0; i < size; i++) {
      pinMode(this.pins[i], INPUT_PULLUP);
    }
    return true;
  }
  void log() override {
    logParent("data");
  }
  void handle() override {
  }
}

void setup() {
  Serial.begin(9600);        // Start serial communication at 9600 bps
  inputString.reserve(200);  // Reserve 200 bytes for the input string
}

void loop() {

  //Handle all devices
  for (i = 0; i < deviceCount; i++) {
    devices[i].handle();
  }

  // Check if a complete string has been received
  if (stringComplete) {
    Serial.print("Received: ");
    Serial.println(inputString);  // Print the received string
    if (inputString[0] == "_") {  //The recieved String is a command
      command = inputString;
    } else {
      if (command) {
        String params[MAX_PARAMETERS];
        int itemCount = splitString(input, ',', params, MAX_PARAMETERS);
        if (command == "_setup") {
          //Setup based on Logging Device ID
          if (params[0] == "20") {  //20 = Wind Direction
            char[] pins[8];
            for (i = 2; i < 10; i++) {
              pins[i - 2] = (char)params[i];
            }
            devices[deviceCount] = new WindDirection(params[0], params[1], pins);
          } else if (params[0] == "21") {

          } else {
            //Logging Device ID not supported by this external microcontroller
          }

          if (devices[deviceCount]) {  //Device Instance was created
            bool iniRes = devices[deviceCount].init();
            if (iniRes) {
              Serial.print("OK");
            } else {
              Serial.print("ERROR");
            }
            deviceCount++;
          }
        } else if (command == "_req") {
        
        }

        command = "";  //Reset command
      } else {
        //No command was previously loaded, handle incoming string otherwise or ignore
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

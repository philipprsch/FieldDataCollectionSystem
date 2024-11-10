
String inputString = "";      // A string to hold incoming data
bool stringComplete = false;  // Whether the string is complete 

void setup() {
  Serial.begin(9600);
  inputString.reserve(200);
}
void splitString(String* input, char delimiter, String* part1, String* part2) {
    String lol = *input;
    int delimiterIndex = lol.indexOf(delimiter);
    if (delimiterIndex != -1) {
        *part1 = lol.substring(0, delimiterIndex);
        *part2 = lol.substring(delimiterIndex + 1);
    } else {
        part1 = input;
        *part2 = ""; // No delimiter found, so part2 is empty
    }
}
struct BrainMethodMap {
    const char* name;
    void (Brain::*func)();
};
class Brain {
  private:

  public:
  Brain() {

  }
  void sendError(String errorID) {
    Serial.println("!ER"+errorID);
  }
  bool handleInput(String input) {
    if (!input[0] == '/') {
      this->sendError("01");
      return false; //or hanlde input ohterwise
    }
    String command, parameters;
    splitString(&input, ' ', &command, &parameters);

  }
};

void loop() {
  if (stringComplete) {
    processInputString(inputString);
    inputString = "";
    stringComplete = false;
  }

}

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
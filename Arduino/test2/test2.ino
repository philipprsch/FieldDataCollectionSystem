
#define MAX_PARAMETERS 10
void setup() {

    Serial.begin(9600);

    String params[MAX_PARAMETERS];

    for (char i = 0; i < MAX_PARAMETERS; i++) {
        params[i] = "";
    }
    

    params[0] = "21";
    params[1] = "21-0";
    params[2] = "2";

    factoryFunction(params);
}


void com_setup(const String params[], char parmCount) {
LoggingDevice* device = factoryMap[i].factory(params);



void factoryFunction(String params[]) {
    for (int i = 0; i < 10; i++) {
        Serial.print("Parameter " + String(i) + ": ");
        Serial.println(params[i]);
    }


    
}

void loop() {
    
}
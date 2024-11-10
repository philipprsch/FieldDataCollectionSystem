
const int ledPin = 13;
void setup() {
    Serial.begin(9600);  // Initialize Serial communication (USB + pins 0 and 1)
    pinMode(ledPin, OUTPUT);
}

void loop() {
    digitalWrite(ledPin, HIGH);
    Serial.println("Testing");
    delay(1000);  // Wait for 1 second
    digitalWrite(ledPin, LOW);
    Serial.println("Testing2");
    delay(1000);  // Wait for 1 second
}
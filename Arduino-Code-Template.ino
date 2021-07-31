const unsigned int BAUDRATE = 9600;
const String MESSAGE = "Hello from the Arduino UNO";

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(BAUDRATE);

  // Wait for the logger to send data.
  // LED on indicates waiting state
  digitalWrite(LED_BUILTIN, HIGH);

  String read_line;
  while (true)
  {
    if(Serial.available())
    { 
      read_line = Serial.readStringUntil('\n');
      break;
    }
  }
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println(read_line);
}

void loop()
{
  Serial.println(MESSAGE);
  delay(2000);
}

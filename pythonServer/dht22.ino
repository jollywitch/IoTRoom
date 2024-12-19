#include <DHT.h>

bool startFlag = false;
bool nextFlag = false;
DHT dht(8, DHT22);

unsigned long previousMillis = 0;
const long interval = 500;

int dataIndex = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  delay(1000);
}

void loop() {
  Serial.flush();
  if (startFlag) {
    unsigned long currentMillis = millis();
    
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;

      float t = dht.readTemperature();
      float h = dht.readHumidity();
      float datas[3] = {t, h, dht.computeHeatIndex(t, h, false)};

      if (dataIndex < 3) {
        Serial.println(datas[dataIndex]);

        unsigned long lastPrintTime = millis();
        while (millis() - lastPrintTime < interval) {
          if (Serial.available()) {
            String input = readSerialInput();
            if (input == "received") {
              nextFlag = true;
              break;
            }
          }
        }

        if (nextFlag) {
          nextFlag = false;
          dataIndex++;
        }
      } else {
        Serial.println("finish");
        startFlag = false;
        nextFlag = false;
        dataIndex = 0;
      }
    }
  }
}

String readSerialInput() {
  String result = "";
  while (Serial.available()) {
    char c = (char)Serial.read();
    result += c;
    delay(10);
  }
  result.trim();
  Serial.println(result);
  return result;
}

void serialEvent() {
  String input = readSerialInput();
  if (input == "start") {
    startFlag = true;
  }
}
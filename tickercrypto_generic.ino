#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "SSD1306Ascii.h"
#include "SSD1306AsciiWire.h"

// Paramètres WiFi
const char* ssid = "ssid";
const char* password = "zePassword";

// Paramètres OLED
#define I2C_ADDRESS 0x3C
#define RST_PIN -1
SSD1306AsciiWire oled;

// Adresse du serveur
const char* serverName = "http://192.168.1.251:1789/";

void setup() {
  Wire.begin(41, 40);
  Wire.setClock(400000L);
  Serial.begin(115200);

#if RST_PIN >= 0
  oled.begin(&Adafruit128x32, I2C_ADDRESS, RST_PIN);
#else
  oled.begin(&Adafruit128x32, I2C_ADDRESS);
#endif

  oled.setFont(Adafruit5x7);
  oled.clear();

  // Connexion WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion au WiFi...");
  }
  Serial.println("Connecté au WiFi !");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    const char* cryptos[] = {"BTC", "ETH", "TRX", "MATIC"};
    oled.clear();
    for (int i = 0; i < 4; i++) {
      //http.begin(serverName + cryptos[i]);
      http.begin(String(serverName) + String(cryptos[i]));

      int httpResponseCode = http.GET();

      if (httpResponseCode > 0) {
        String payload = http.getString();
        Serial.println(cryptos[i] + String(": ") + payload);
        
        oled.set1X();
        oled.print(cryptos[i] + String(": "));
        oled.println(payload);
      } else {
        Serial.print("Erreur HTTP: ");
        Serial.println(httpResponseCode);
        oled.println("Erreur HTTP");
      }
      http.end();
      delay(1000); // Pause entre les requêtes
    }
  } else {
    Serial.println("Erreur WiFi. Tentative de reconnexion...");
    WiFi.begin(ssid, password);
  }
  delay(300000);  // Pause de 5 minutes avant de refaire une requête
}

#include <WiFiS3.h>
#include <WiFiSSLClient.h>
#include <ArduinoHttpClient.h>
#include "arduino_secrets.h"  // contains SECRET_SSID and SECRET_PASS

#define BAUD_RATE 9600
#define SAMPLE_RATE 256
#define INPUT_PIN A0

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
String deploymentID = "AKfycbzNPxN0WaeT8JAaTpunYVVO9UPkyM1xnRvkLzQ39CwrntdOrUqD5qfB52kVFtHsoYZr";  // 👈 Replace this

char server[] = "script.google.com";

WiFiSSLClient wifi;
HttpClient client = HttpClient(wifi, server, 443);

// === Signal conversion parameters ===
const float Vref = 5.0;
const int ADC_resolution = 1024;
const float Gain = 1000.0;

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial);

  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("WiFi module not detected.");
    while (true);
  }

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to: ");
    Serial.println(ssid);
    WiFi.begin(ssid, pass);
    delay(3000);
  }

  Serial.println("Connected to WiFi.");
}

void loop() {
  static unsigned long past = 0;
  unsigned long now = micros();
  unsigned long elapsed = now - past;
  past = now;

  static long timer = 0;
  timer -= elapsed;

  if (timer < 0) {
    timer += 1000000 / SAMPLE_RATE;

    // === Read and compute ===
    int raw_adc = analogRead(INPUT_PIN);
    float eeg_uv = ((float)raw_adc / ADC_resolution) * Vref / Gain * 1e6;  // microvolts
    float eeg_filtered = EEGFilter(eeg_uv);

    // === Send to Google Sheets ===
    // Construct request URL with raw, uv, and filtered
    String url = "/macros/s/" + deploymentID + "/exec?raw=" + raw_adc + "&uv=" + eeg_uv +"&filtered=" + eeg_filtered;

    Serial.print("Sending to: ");
    Serial.println(url);

    client.get(url);

    int statusCode = client.responseStatusCode();
    String response = client.responseBody();

    Serial.print("Status code: ");
    Serial.println(statusCode);
    Serial.print("Response: ");
    Serial.println(response);
    Serial.println("----");
  }
}

// === Bandpass Filter (0.5–29.5 Hz) ===
float EEGFilter(float input) {
  float output = input;

  static float z1a, z2a, z1b, z2b, z1c, z2c, z1d, z2d;

  // Section 1
  float x1 = output - -0.95391350 * z1a - 0.25311356 * z2a;
  output = 0.00735282 * x1 + 0.01470564 * z1a + 0.00735282 * z2a;
  z2a = z1a; z1a = x1;

  // Section 2
  float x2 = output - -1.20596630 * z1b - 0.60558332 * z2b;
  output = 1.00000000 * x2 + 2.00000000 * z1b + 1.00000000 * z2b;
  z2b = z1b; z1b = x2;

  // Section 3
  float x3 = output - -1.97690645 * z1c - 0.97706395 * z2c;
  output = 1.00000000 * x3 - 2.00000000 * z1c + 1.00000000 * z2c;
  z2c = z1c; z1c = x3;

  // Section 4
  float x4 = output - -1.99071687 * z1d - 0.99086813 * z2d;
  output = 1.00000000 * x4 - 2.00000000 * z1d + 1.00000000 * z2d;
  z2d = z1d; z1d = x4;

  return output;
}


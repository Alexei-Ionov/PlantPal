#include <Arduino.h>
#include <WiFi.h>
#include "esp_http_client.h"
#include <cstring>
const char* ssid = "YourSSID";
const char* password = "YourPassword";
const int sensor_pin = 34;
WiFiServer server(8080);  // Listen on port 8080
String TOKEN = "";
const char* api_endpoint = "http://192.168.1.74:5000/update_sensor_reading"

void setup() {
    Serial.begin(115200);
    //set the resolution to 12 bits (0-4095)
    analogReadResolution(12);
    Serial.print("Connecting to WIFI...");
    WiFi.begin(ssid, password);
  
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("...");
    }
    Serial.println("Connected to WiFi");

    // Print IP address
    Serial.print("ESP32 IP address: ");
    Serial.println(WiFi.localIP());

    server.begin();  // Start the TCP server
    Serial.println("Server started");
}

void perform_post_request(String soil_moisture) {
    esp_http_client_config_t config = {
        .url = api_endpoint,
    };
    esp_http_client_handle_t client = esp_http_client_init(&config);
    String post_data = "soil_moisture=" + soil_moisture + "&token=" + TOKEN
    // const char *post_data = "soil_moisture=value1&token=value2";
    esp_http_client_set_url(client, api_endpoint);
    esp_http_client_set_method(client, HTTP_METHOD_POST);
    esp_http_client_set_post_field(client, post_data, strlen(post_data));

    esp_err_t err = esp_http_client_perform(client);
    if (err == ESP_OK) {
        printf("HTTP POST Status = %d, content_length = %d\n",
               esp_http_client_get_status_code(client),
               esp_http_client_get_content_length(client));
    } else {
        printf("HTTP POST request failed: %s\n", esp_err_to_name(err));
    }
    esp_http_client_cleanup(client);
}

void loop() {
    WiFiClient client = server.available();  // Check for incoming clients
    if (client) {
        Serial.println("Client connected");
        while (client.connected()) {
            if (client.available()) {
                String token = client.readStringUntil('\n');
                TOKEN = token;
                // memcpy((void*)TOKEN, )
                Serial.println("Received token: " + token);
                client.println("Token received");  // Respond to client
            }
        }
        client.stop();
        Serial.println("Client disconnected");
    }
    if (TOKEN != "") { 
      int sensorValue = analogRead(sensorPin);  // Read the analog value (0-4095)
      
      // Convert the analog reading to voltage (0 to 3.3V)
      float voltage = sensorValue * (3.3 / 4095.0);
      
      // Convert the voltage to a scale of 0.0 to 10.0
      float moistureLevel = (voltage / 3.3) * 10.0;  // Scale voltage to 0.0 - 10.0

      Serial.print("moisture level:")
      Serial.println(moistureLevel);

      String soil_moisture = String(moistureLevel);
      perform_post_request(soil_moisture)

      delay(100);  // delay in between reads for clear read from serial
    }
    
    
}
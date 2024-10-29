#include <WiFi.h>
#include <NetworkClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <Arduino.h>
#include <ArduinoJson.h> //need to install
#include "esp_http_client.h"
#include <cstring>
const char* ssid = "Kool-Kaa";
const char* password = "tolstoywinter";
const int sensor_pin = 34;
// String TOKEN = "7f1f3a06-9ab4-46ec-823a-3cd1bfc61f48";
String TOKEN = "";
const char* api_endpoint = "http://192.168.1.74:6969/update_sensor_reading";
const int DELAY = 60000; //delay of 1 minute for sending data to server

const unsigned long interval = 60000;  // 1 minute intervals b/w post request wiht sensor readings
unsigned long previousMillis = 0;     // stores the last time the action was performed

WebServer server(80);

void handleCORS() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
}
void handleConnect() {
  Serial.println("Accepted client request!");
  handleCORS();  // Set CORS headers for the response
  if (server.method() == HTTP_POST) {  // make sure it's a post req
    
    if (server.hasArg("plain")) {      // Read the plain text from the body
      String body = server.arg("plain"); // Get the body content
      

      // Parse the JSON body
      StaticJsonDocument<200> jsonDoc;
      DeserializationError error = deserializeJson(jsonDoc, body);
      if (error) {
        server.send(400, "application/json", "{\"message\": \"Invalid JSON\"}");
        return;
      }

      // Check if the token matches
      String receivedToken = jsonDoc["token"];
      TOKEN = receivedToken;
      server.send(200, "application/json", "{\"message\": \"Token accepted. Connected to ESP32.\"}");
      Serial.println("ESP recieved token successfully");
    } else {
      server.send(400, "application/json", "{\"message\": \"Missing token .\"}");
    }
  } else if (server.method() == HTTP_OPTIONS) { 
    server.send(204); //nothing really needs to be sent back
  } else {
    server.send(405, "text/plain", "Method Not Allowed");
  }
}


void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

void perform_post_request(String soil_moisture) {
    esp_http_client_config_t config = {
        .url = api_endpoint,
    };
    esp_http_client_handle_t client = esp_http_client_init(&config);

    // Create JSON object for POST data
    StaticJsonDocument<200> jsonDoc;
    jsonDoc["soil_moisture"] = soil_moisture;
    jsonDoc["token"] = TOKEN;

    // Convert JSON object to string
    String post_data;
    serializeJson(jsonDoc, post_data);

    // Set up the HTTP request
    esp_http_client_set_method(client, HTTP_METHOD_POST);
    esp_http_client_set_post_field(client, post_data.c_str(), post_data.length());
    esp_http_client_set_header(client, "Content-Type", "application/json");

    // Perform the HTTP request
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

void setup(void) {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp32")) {
    Serial.println("MDNS responder started");
  }

  server.on("/connect", handleConnect);

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  unsigned long currentMillis = millis();  // get the current time

  // Check if the interval has passed
  if (currentMillis - previousMillis >= interval) {
    if (TOKEN != "") { 
      float moistureLevel = 6.9;
      Serial.print("moisture level:");
      Serial.println(moistureLevel);

      String soil_moisture = String(moistureLevel);
      perform_post_request(soil_moisture);
      previousMillis = currentMillis;
    }
  }
  delay(2);  //allow the cpu to switch to other tasks
}

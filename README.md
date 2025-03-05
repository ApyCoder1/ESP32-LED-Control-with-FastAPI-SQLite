
---

## ESP32 LED Control with FastAPI SQLite  

This project is a web-based LED control system using an ESP32, FastAPI, and SQLite. The ESP32 communicates with a FastAPI server to toggle and retrieve LED states stored in a database.

### Features  
- Control 3 LEDs connected to an ESP32 via a FastAPI web dashboard  
- LED states are stored in an SQLite database  
- Interactive UI with real-time LED status  
- REST API for getting and setting LED states  

---

## 🛠 Setup Instructions  

### 1️⃣ FastAPI Server  

#### Install Dependencies  
```bash
pip install fastapi uvicorn pydantic sqlite3
```

#### Run the Server  
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
```bash
http://127.0.0.1:8000/
```
This will start the FastAPI server on port `8000`.  


---

### 2️⃣ ESP32 Arduino Code  

Upload the following sketch to your ESP32. This code sends HTTP requests to the FastAPI server to fetch and update LED states.  

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "ApyCoder";     // Replace with your WiFi SSID
const char* password = "Asif12345";  // Replace with your WiFi Password
const char* serverUrl = "http://10.129.101.93:8000/led";  // FastAPI server URL

// GPIO pins connected to the LEDs (Updated to D10, D9, D8)
const int ledPins[3] = {10, 9, 8};  

void setup() {
    Serial.begin(115200);

    // Initialize LED pins as OUTPUT
    for (int i = 0; i < 3; i++) {
        pinMode(ledPins[i], OUTPUT);
        digitalWrite(ledPins[i], LOW);  // Ensure all LEDs are off at the start
    }

    // Connect to WiFi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi!");
}

void loop() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverUrl);  // HTTP request to the FastAPI server
        int httpCode = http.GET();  // Send GET request

        if (httpCode == 200) {  // Successful response
            String payload = http.getString();  // Get the response string
            Serial.println("Response: " + payload);

            // Parse JSON response
            StaticJsonDocument<200> doc;
            deserializeJson(doc, payload);

            // Loop through each LED and update the state based on the response
            for (int i = 0; i < 3; i++) {
                int ledState = doc["leds"][i]["state"];  // Get the state for each LED
                if (ledState == 1) {
                    digitalWrite(ledPins[i], HIGH);  // Turn ON LED
                } else {
                    digitalWrite(ledPins[i], LOW);   // Turn OFF LED
                }
            }

        } else {
            Serial.println("Failed to get LED state");
        }

        http.end();  // Close HTTP connection
    } else {
        Serial.println("WiFi Disconnected! Reconnecting...");
        WiFi.begin(ssid, password);  // Reconnect to WiFi
    }

    delay(2000);  // Fetch LED state every 2 seconds
}

```

Replace `YOUR_WIFI_SSID`, `YOUR_WIFI_PASSWORD`, and `YOUR_SERVER_IP` with your actual WiFi credentials and server IP.

---

## 📡 API Endpoints  

| Method | Endpoint         | Description                 |
|--------|-----------------|-----------------------------|
| `GET`  | `/led/{id}`      | Get state of a specific LED |
| `POST` | `/led/{id}`      | Set state of a specific LED |
| `GET`  | `/led`           | Get all LED states         |



---

## 📷 UI Preview  

The web dashboard provides a simple interface to toggle LEDs:  
![image](https://github.com/user-attachments/assets/8dee7bf9-9668-4127-9efb-b56c1b285057)
![image](https://github.com/user-attachments/assets/933f6963-088f-47e1-8deb-82392e192d70)



---

## 🚀 Future Improvements   
- Implement MQTT for better IoT communication  

---

## 📜 License  
This project is open-source under the MIT License.  

---

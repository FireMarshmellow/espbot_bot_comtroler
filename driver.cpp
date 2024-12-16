#include <esp_now.h>
#include <WiFi.h>
#include <ESP32Servo.h>
#include <HardwareSerial.h>

// *****************************
// Pins and Constants
// *****************************

// Define servo pins
#define SERVO1_PIN 12
#define SERVO2_PIN 14
#define REGULAR_SERVO_PIN 13

// Define RGB LED pins
#define LED_RED_PIN 27
#define LED_GREEN_PIN 26
#define LED_BLUE_PIN 25

// Define UART pins for DFRobot Voice Prompt Module
#define RXD2 16
#define TXD2 17

// Data packet structure
struct DataPacket {
  int x;
  int y;
  int sw;
  int btn1;
  int btn2;
  int btn3;
  int btn4;
  int btn5;
};

DataPacket data;

// Create servo objects
Servo servo1;
Servo servo2;
Servo regularServo;

// Constants
const int THRESHOLD = 3000;
const int REST_X = 32767;
const int REST_Y = 32767;

// *****************************
// DFRobot Voice Prompt Functions
// *****************************

HardwareSerial mySerial(1); // Serial2 for voice module

void send_command(uint8_t command[], size_t length) {
  for (size_t i = 0; i < length; i++) {
    mySerial.write(command[i]);
  }
}

void play_track(uint8_t track_number) {
  // Adjust command as needed for your DFRobot module
  uint8_t command[] = {0x7E, 0x03, 0x00, 0x02, 0x00, track_number, 0xEF};
  send_command(command, sizeof(command));
}

void set_volume(uint8_t level) {
  if (level > 30) {
    Serial.println("Volume level must be between 0 and 30.");
    return;
  }
  uint8_t command[] = {0x7E, 0x06, 0x00, 0x02, 0x00, level, 0xEF};
  send_command(command, sizeof(command));
}

// You can add more commands (next_track, pause, etc.) as needed from your esp_player code.

// *****************************
// Utility Functions
// *****************************

// Set RGB LED color
void setColor(bool red, bool green, bool blue) {
  digitalWrite(LED_RED_PIN, red);
  digitalWrite(LED_GREEN_PIN, green);
  digitalWrite(LED_BLUE_PIN, blue);
}

// Control continuous servos (0-180 as "speed")
void controlServos(int servo1Speed, int servo2Speed) {
  servo1.write(servo1Speed);
  servo2.write(servo2Speed);
}

// Control a regular servo
void controlRegularServo(int angle) {
  regularServo.write(angle);
}

// Joystick output handler
void joystickOutput(int x, int y, int sw, int btn1, int btn2, int btn3, int btn4, int btn5) {
  if (sw == 0) {
    // Joystick switch pressed: manipulate the regular servo angle
    int angle = 60 + ((REST_X - x) * 60) / REST_X;
    controlRegularServo(angle);

    // Set LED color based on x value
    if (x > REST_X) {
      setColor(1, 1, 1);  // White
    } else {
      setColor(1, 1, 0);  // Yellow
    }

  } else {
    // Joystick switch not pressed
    controlRegularServo(90); // default position

    if (x < REST_X - THRESHOLD) {
      setColor(1, 0, 1);  // Magenta
      controlServos(40, 40);
    } else if (x > REST_X + THRESHOLD) {
      setColor(0, 1, 1);  // Cyan
      controlServos(100, 100);
    } else if (y < REST_Y - THRESHOLD) {
      setColor(0, 1, 0);  // Green
      controlServos(100, 40);
    } else if (y > REST_Y + THRESHOLD) {
      setColor(1, 0, 0);  // Red
      controlServos(40, 100);
    } else {
      // No significant movement: stop servos and turn off LED
      controlServos(90, 90);
      setColor(0, 0, 0);
    }
  }

  // Play sounds if buttons are pressed
  // Here we simply map each button to a specific track number.
  // Adjust track numbers as per your module's SD card setup.
  if (btn1 == 1) play_track(1);
  if (btn2 == 1) play_track(2);
  if (btn3 == 1) play_track(3);
  if (btn4 == 1) play_track(4);
  if (btn5 == 1) play_track(5);
}

// ESP-NOW data receive callback
void onDataReceive(const esp_now_recv_info_t *recvInfo, const uint8_t *incomingData, int len) {
  if (len == sizeof(data)) {
    memcpy(&data, incomingData, sizeof(data));

    // Print received data for debugging
    Serial.print("Joystick X: ");
    Serial.print(data.x);
    Serial.print(" | Y: ");
    Serial.print(data.y);
    Serial.print(" | SW: ");
    Serial.print(data.sw);
    Serial.print(" | BTN1: ");
    Serial.print(data.btn1);
    Serial.print(" | BTN2: ");
    Serial.print(data.btn2);
    Serial.print(" | BTN3: ");
    Serial.print(data.btn3);
    Serial.print(" | BTN4: ");
    Serial.print(data.btn4);
    Serial.print(" | BTN5: ");
    Serial.println(data.btn5);

    joystickOutput(data.x, data.y, data.sw, data.btn1, data.btn2, data.btn3, data.btn4, data.btn5);
  } else {
    Serial.println("Received data length mismatch.");
  }
}

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  Serial.println("Hello, world!");

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  WiFi.setChannel(6);

  // Print out the MAC address so it can be used on the remote side
  Serial.print("Driver device MAC: ");
  Serial.println(WiFi.macAddress());

  // Initialize servo objects
  servo1.attach(SERVO1_PIN);
  servo2.attach(SERVO2_PIN);
  regularServo.attach(REGULAR_SERVO_PIN);

  // Initialize RGB LED pins
  pinMode(LED_RED_PIN, OUTPUT);
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_BLUE_PIN, OUTPUT);
  setColor(0, 0, 0);  // Turn off LED initially

  // Set servos to initial positions
  controlServos(90, 90);
  controlRegularServo(90);

  // Initialize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Register the receive callback
  esp_now_register_recv_cb(onDataReceive);

  // Initialize the DFRobot Voice Prompt Module serial
  mySerial.begin(9600, SERIAL_8N1, RXD2, TXD2);
  delay(1000); // Give the module some time to initialize

  // Optionally set initial volume
  set_volume(10);

  // Print confirmation of initialization
  Serial.println("ESP-NOW Driver is ready on Channel 6 and listening for data...");
}

void loop() {
  // Nothing to do here; data is handled in the callback
}

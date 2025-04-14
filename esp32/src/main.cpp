#include <Arduino.h>
#include <WiFi.h>
#define LED1 2
#define BLINK_SPEED_MS 200
#define BUTTON_PIN 3

bool button_pressed() {
  // TODO: debouncing
  static bool was_pressed = false;
  bool is_pressed = digitalRead(BUTTON_PIN);

  if (is_pressed && !was_pressed) {
    was_pressed = true;
    return true;
  } else if (!is_pressed) {
    was_pressed = false;
  }
  return false;
}

void blink_task(void *arg) {
  while (true) {
    digitalWrite(LED1, HIGH);
    vTaskDelay(pdMS_TO_TICKS(BLINK_SPEED_MS));
    digitalWrite(LED1, LOW);
    vTaskDelay(pdMS_TO_TICKS(BLINK_SPEED_MS));
  }
}

TaskHandle_t Blink_Task;
TaskHandle_t Send_Request_Task;

void setup() {
  pinMode(LED1, OUTPUT);
  Serial.begin(9600);
  xTaskCreatePinnedToCore(blink_task,  /* Function to implement the task */
                          "blink",     /* Name of the task */
                          2048,       /* Stack size in words */
                          NULL,        /* Task input parameter */
                          0,           /* Priority of the task */
                          &Blink_Task, /* Task handle. */
                          0);          /* Core where the task should run */
}

void loop() {
  if (button_pressed()) {
    // Send request
    // while sending request blink led
  }
}

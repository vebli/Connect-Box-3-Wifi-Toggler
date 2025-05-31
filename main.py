import RPi.GPIO as GPIO
import time 
import subprocess

led_pin = 17
switch_pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def toggle_wifi():
    subprocess.call(["python3", "toggle_wifi.py"])

try:
    while True:
        if GPIO.input(switch_pin) == GPIO.LOW:
            GPIO.output(led_pin, GPIO.HIGH)
            toggle_wifi()
            time.sleep(1)

except KeyboardInterrupt:
    pass
finally: 
    GPIO.cleanup()

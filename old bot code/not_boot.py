import network
import socket
import time
from machine import Pin, PWM

# Configure Wi-Fi Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32', password='mypassword')

# Wait for the access point to start
time.sleep(2)

# Configure the socket
addr = socket.getaddrinfo('0.0.0.0', 5005)[0][-1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(addr)

print('Listening on', addr)

# Initialize continuous servos
servo1 = PWM(Pin(12), freq=50)
servo2 = PWM(Pin(32), freq=50)
regular_servo = PWM(Pin(27), freq=50)

sfx_0 = Pin(22, Pin.OUT, Pin.PULL_UP)
sfx_1 = Pin(21, Pin.OUT, Pin.PULL_UP)
sfx_2 = Pin(19, Pin.OUT, Pin.PULL_UP)
sfx_3 = Pin(18, Pin.OUT, Pin.PULL_UP)
sfx_4 = Pin(5, Pin.OUT, Pin.PULL_UP)
sfx_5 = Pin(4, Pin.OUT, Pin.PULL_UP)
sfx_6 = Pin(2, Pin.OUT, Pin.PULL_UP)
sfx_7 = Pin(15, Pin.OUT, Pin.PULL_UP)

# Define pins for each color
led_pins = {color: Pin(pin, Pin.OUT) for color, pin in zip(["red", "green", "blue"], [33, 25, 26])}

# Set initial state of RGB LED to OFF
for pin in led_pins.values():
    pin.off()

def Set_pins_defolt():
    Pin(22, Pin.OUT, Pin.PULL_UP).on()
    Pin(21, Pin.OUT, Pin.PULL_UP).on()
    Pin(19, Pin.OUT, Pin.PULL_UP).on()
    Pin(18, Pin.OUT, Pin.PULL_UP).on()
    Pin(5, Pin.OUT, Pin.PULL_UP).on()
    Pin(4, Pin.OUT, Pin.PULL_UP).on()
    Pin(2, Pin.OUT, Pin.PULL_UP).on()
    Pin(15, Pin.OUT, Pin.PULL_UP).on()

# Threshold to determine joystick direction
THRESHOLD = 3000

# Resting position values for X and Y axes
REST_X = 32767
REST_Y = 32767



def play_sound(pin):
    pin.off()
    time.sleep(0.5)
    pin.on()

Set_pins_defolt()

# Function to control servos
def control_servos(servo1_speed, servo2_speed):
    servo1.duty(servo1_speed)
    servo2.duty(servo2_speed)

def control_regular_servo(angle):
    duty_cycle = int(40 + (angle * 100 / 180))
    regular_servo.duty(duty_cycle)

# Define a function to set the color of the RGB LED
def set_color(red, green, blue):
    for color, state in zip(["red", "green", "blue"], [red, green, blue]):
        led_pins[color].value(state)

def joystick_output(x, y, sw, btn1, btn2, btn3, btn4):
    if sw == 0:
        angle = int(60 + ((REST_X - x) / REST_X) * 60)
        control_regular_servo(angle)
        print(angle)
        set_color(1, 1, x > REST_X)  # White if x > REST_X else Yellow
    else:
        control_regular_servo(90)
        if x < REST_X - THRESHOLD:
            print("Left")
            set_color(1, 0, 1)  # Magenta
            control_servos(40, 40)
        elif x > REST_X + THRESHOLD:
            print("Right")
            set_color(0, 1, 1)  # Cyan
            control_servos(100, 100)
        elif y < REST_Y - THRESHOLD:
            print("Up")
            set_color(0, 1, 0)  # Green
            control_servos(100, 40)
        elif y > REST_Y + THRESHOLD:
            print("Down")
            set_color(1, 0, 0)  # Red
            control_servos(40, 100)
        else:
            control_servos(0, 0)
            set_color(0, 0, 0)  # Off
    if btn1 == 1:
        play_sound(sfx_0)
    if btn2 == 1:
        play_sound(sfx_1)
    if btn3 == 1:
        play_sound(sfx_2)
    if btn4 == 1:
        play_sound(sfx_3)
    
            
        

while True:
    try:
        data, addr = s.recvfrom(1024)
        print(data)
        x, y, sw, btn1, btn2, btn3, btn4 = map(int, data.decode().split(','))
        joystick_output(x, y, sw, btn1, btn2, btn3, btn4)
    except OSError as e:
        print("Error: ", e)
        control_servos(0, 0)
        print("Controller disconnected. Retrying...")
        time.sleep(5)  # wait for 5 seconds before retrying

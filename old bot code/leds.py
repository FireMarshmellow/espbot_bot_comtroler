from machine import Pin, PWM
import time

# Define the PWM objects connected to the RGB LED
red = PWM(Pin(26))    # Connect the red pin of the RGB LED to GPIO0
green = PWM(Pin(25))  # Connect the green pin of the RGB LED to GPIO1
blue = PWM(Pin(33))   # Connect the blue pin of the RGB LED to GPIO2

# Set the frequency for the PWM signals
red.freq(1000)
green.freq(1000)
blue.freq(1000)

# Function to set the LED color
def set_color(r, g, b):
    red.duty_u16(r)
    green.duty_u16(g)
    blue.duty_u16(b)

# Loop forever
while True:
    # Red
    set_color(65535, 0, 0)
    time.sleep(1)
    
    # Green
    set_color(0, 65535, 0)
    time.sleep(1)
    
    # Blue
    set_color(0, 0, 65535)
    time.sleep(1)
    
    # Yellow (Red + Green)
    set_color(65535, 65535, 0)
    time.sleep(1)
    
    # Cyan (Green + Blue)
    set_color(0, 65535, 65535)
    time.sleep(1)
    
    # Magenta (Red + Blue)
    set_color(65535, 0, 65535)
    time.sleep(1)
    
    # White (Red + Green + Blue)
    set_color(65535, 65535, 65535)
    time.sleep(1)


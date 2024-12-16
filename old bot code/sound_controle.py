import time
from machine import Pin

sfx_0 = Pin(22, Pin.OUT, Pin.PULL_UP)
sfx_1 = Pin(21, Pin.OUT, Pin.PULL_UP)
sfx_2 = Pin(19, Pin.OUT, Pin.PULL_UP)
sfx_3 = Pin(18, Pin.OUT, Pin.PULL_UP)
sfx_4 = Pin(5, Pin.OUT, Pin.PULL_UP)
sfx_5 = Pin(4, Pin.OUT, Pin.PULL_UP)
sfx_6 = Pin(2, Pin.OUT, Pin.PULL_UP)
sfx_7 = Pin(15, Pin.OUT, Pin.PULL_UP)

def play_sound(pin):
    pin.off()
    time.sleep(0.5)
    pin.on()

def Set_pins_defolt():
    Pin(22, Pin.OUT, Pin.PULL_UP).on()
    Pin(21, Pin.OUT, Pin.PULL_UP).on()
    Pin(19, Pin.OUT, Pin.PULL_UP).on()
    Pin(18, Pin.OUT, Pin.PULL_UP).on()
    Pin(5, Pin.OUT, Pin.PULL_UP).on()
    Pin(4, Pin.OUT, Pin.PULL_UP).on()
    Pin(2, Pin.OUT, Pin.PULL_UP).on()
    Pin(15, Pin.OUT, Pin.PULL_UP).on()
    

# Main loop
while True:
    play_sound(sfx_0)
    time.sleep(5)
    
    

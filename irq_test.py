import machine
from machine import Pin
import time
import uasyncio

class LoggingDev():
    def __init__(self):
        self.interuptFlag = False
        self.debounce_time = 0
        self.pin = Pin(5, Pin.IN, Pin.PULL_UP)
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.callback)
    
    def callback(self, pin):
        if (time.ticks_ms()-self.debounce_time > 500):
            self.interuptFlag = True
            self.debounce_time = time.ticks_ms()

    async def handle(self):
        while True:
            if self.interuptFlag:
                print("Button pressed")
                self.interuptFlag = False
            await uasyncio.sleep_ms(800)

myLoggingDev  = LoggingDev()
async def main():

    uasyncio.create_task(myLoggingDev.handle())

    while True:
        await uasyncio.sleep(2)
        print("Doing something")

uasyncio.run(main())

# def callback(pin):
#     print("callback")

# pin = Pin(5, Pin.IN, Pin.PULL_UP)
# pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)

# while True:
#     time.sleep(2)
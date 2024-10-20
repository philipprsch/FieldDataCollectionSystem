from machine import Pin
from time import sleep
import os
import uasyncio

led = Pin("LED", Pin.OUT)

async def blink():
    while True:
        led.toggle()
        await uasyncio.sleep_ms(500)

loop = uasyncio.get_event_loop()
loop.create_task(blink())
loop.run_forever()
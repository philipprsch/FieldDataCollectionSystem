import machine
from machine import Pin
import time
import uasyncio


led = Pin("LED", Pin.OUT)
btn = Pin(11, Pin.IN, Pin.PULL_DOWN)

async def blink():
    while True:
        led.toggle()
        await uasyncio.sleep_ms(500)

timeInit = time.time() 

def report():
    print(f'Button pressed! at {time.time() - timeInit} seconds')

async def checkButton():
    btn_prev = btn.value()
    while (btn.value() == 1) or (btn.value() == btn_prev):
        btn_prev = btn.value()
        await uasyncio.sleep_ms(100)

async def buttion_coroutine():
    while True:
        await checkButton()
        report()

async def main():
    uasyncio.create_task(blink())
    uasyncio.create_task(buttion_coroutine())

    while True:
        await uasyncio.sleep(500)  # let other tasks run

uasyncio.run(main())
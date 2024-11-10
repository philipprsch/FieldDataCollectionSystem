import uasyncio as asyncio
import machine
from machine import RTC, Pin
import uos  # Use uos instead of os for MicroPython
import time

import lib.sdcard as sdcard
from lib.ds1307 import DS1307 #External RTC Module
from lib.task_manager import TaskManager

from helpers import read_json, dynamic_import, append_to_file, read_file, does_folder_exist, get_readable_time, get_i2c_instance, log_exception, get_UART_instance


#--------MY IMPORTS-------------------------------------
from devices.LoggingDevice import LoggingDevice
#from modules.DHT11_LoggingDevice import DHT11_LoggingDevice


#Read LoggingDevices file
logging_devices = read_json("lookup/LoggingDevices.json")
print(logging_devices)

rtc = RTC() #Use onbaord Pico RTC, can be supplemented by external RTC Module


config = read_json("config/config.json")
if config is None: 
    e = OSError("No configuration file found")
    log_exception(e)
    raise e


if (config != None and config["others"]["external_rtc"]):
    #Initialize and update onboard RTC module
    rtc_i2c = get_i2c_instance(1, 15, 14, freq=400000)
    ext_rtc = DS1307(rtc_i2c)
    ext_rtc.halt(False) # 32 khz crystal enable
    rtc.datetime(ext_rtc.datetime())

spi = machine.SPI(0,
                  baudrate=100000,
                  polarity=0,
                  phase=0,
                  sck=machine.Pin(18),
                  mosi=machine.Pin(19),
                  miso=machine.Pin(16))

cs = machine.Pin(17, machine.Pin.OUT)

# Initialize the SD card
sd = sdcard.SDCard(spi, cs)



# Mount the SD card onto the file system
vfs = uos.VfsFat(sd)
if (not does_folder_exist("/sd")):
    uos.mount(vfs, "/sd")

task_manager = TaskManager()

arduino = get_UART_instance(0) #Get Bus 0 Serial Instance to read arduino prints for debugging
myLoggingDevices = []

#For Arduino Debugging
arduinoInput = ""

async def main():
    if config is not None:
        for device in config["loggingDevices"]:
            #print(device)
            myLoggingDevices.append(LoggingDevice.create_instance(device["id"], **(device["constructor_args"] | {'alias': device["alias"]})))

    while True:
        #await task_manager.list_tasks()
        #Listen to Arduino
        if arduino.any():
            res = arduino.read()
            if res.decode() == "\n":
                print("Ard: "+arduinoInput)
                arduinoInput = ""
            else:
                arduinoInput += res.decode()

        await asyncio.sleep(1)

# Run the event loop
try:
    asyncio.run(main())
except Exception as e: #Fatal exception
    log_exception(e, rtc.datetime())
    error_led = Pin("LED", Pin.OUT)
    for i in range(0, 5):
        error_led.on()
        time.sleep_ms(250)
        error_led.off()
        time.sleep_ms(250)
    machine.reset()

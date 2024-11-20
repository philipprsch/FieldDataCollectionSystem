
import uasyncio as asyncio
import machine
from machine import Pin
import uos  # Use uos instead of os for MicroPython
import time
from lib.SafeDict import SafeDict
import lib.sdcard as sdcard
from lib.ds1307 import DS1307 #External RTC Module
from lib.task_manager import TaskManager
from defines import *
from helpers import read_json, dynamic_import, append_to_file, read_file, does_folder_exist, get_readable_time, get_i2c_instance, get_UART_instance
from lib.Debugger import MyDebugger
from lib.Communicator import Communicator
from lib.Config import Config
import lib.Config as conf

#--------MY IMPORTS-------------------------------------
from devices.LoggingDevice import LoggingDevice, LoggingDeviceInitFailed

from devices.DHT11_LoggingDevice import *
from devices.otherLoggingDevices import *
from devices.Regenmesser_LoggingDevice import *
from devices.WindDirection_LoggingDeviceS import *
from devices.WindSpeed_LoggingDeviceS import *

# _ = WindDirection_LoggingDeviceSerial
# _ = WindSpeed_LoggingDeviceSerial

#from modules.DHT11_LoggingDevice import DHT11_LoggingDevice


if (Config.config.get("others", "external_rtc", fb=False)):
    #Initialize and update onboard RTC module
    rtc_i2c = get_i2c_instance(1, 15, 14, freq=400000)
    conf.rtc = DS1307(rtc_i2c)
    conf.rtc.halt(False) # 32 khz crystal enable
    
print("Datetime is:" + get_readable_time(conf.rtc.datetime()))

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
if (not does_folder_exist(PATH_SD_CARD_MOUNT)):
    uos.mount(vfs, PATH_SD_CARD_MOUNT)


myLoggingDevices = []
#time.sleep(1) #Wait for Arduino startup (LED Flashing)

async def main():
    logging_devices = Config.config.get("loggingDevices")
    print(logging_devices)
    if logging_devices is not None:
        for device in logging_devices:
            if (not device["alias"]): raise ValueError("Device does not feature 'alias' attribute in configuration file")
            if (not device["id"]): raise ValueError(f"Device {device['alias']} does not feature 'id' attribute in configuration file")
            if (not device["constructor_args"]): raise ValueError(f"Device {device['alias']} does not feature 'constructor_args' attribute in configuration file")
            #print(device)
            try:
                new_instance = LoggingDevice.create_instance(device["id"], **(Config.lookup_ld.get(device["id"], "constructor_arg_defaults", fb={}) | device["constructor_args"] | {'alias': device["alias"]}))
            except LoggingDeviceInitFailed as e:
                MyDebugger.logException(e)
            else:
                myLoggingDevices.append(new_instance)

    #Print all devices set up on the Pico
    MyDebugger.log("Listing Local Devices:")
    for device in myLoggingDevices:
        MyDebugger.log(f"Logging Device: {device.alias}, Type: {device.__class__.__name__}, ID: {device.id} Interval: {device.interval}")
        

    #Print all Devices setup on each controller
    controllers = Config.config.get("controllers")
    if controllers is not None:
        for alias in controllers.keys():
            com = Communicator(alias)
            MyDebugger.log(f"Conroller {alias} Device List: \n {com.list()}")
    
    MyDebugger.log(await TaskManager.list_tasks())

    while True:
        await asyncio.sleep(10)

# Run the event loop
try:
    asyncio.run(main())
except Exception as e: #Fatal exception
    raise #TODO: Just temporary, remove after testing
    #MyDebugger.logException(e)
    error_led = Pin("LED", Pin.OUT)
    for i in range(0, 5):
        error_led.on()
        time.sleep_ms(250)
        error_led.off()
        time.sleep_ms(250)
    machine.reset()

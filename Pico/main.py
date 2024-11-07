import uasyncio as asyncio
import machine

import ujson
import lib.sdcard as sdcard
import uos  # Use uos instead of os for MicroPython
from machine import RTC, Pin, ADC, UART
import time
from lib.ds1307 import DS1307 #External RTC Module
from task_manager import TaskManager
from helpers import read_json, dynamic_import, append_to_file, read_file, does_folder_exist, get_readable_time, get_i2c_instance, log_exception, get_UART_instance
import dht 
from accelerometer import MPU6050_Accelerometer
#Read LoggingDevices file
logging_devices = read_json("lookup/LoggingDevices.json")
print(logging_devices)

config = read_json("config/config.json")
if config is None: raise OSError("No configuration file found")

rtc = RTC() #Use onbaord Pico RTC, can be supplemented by external RTC Module

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

# Function to register child classes
def register_child(cls):
    # Check if the class has 'class_id' and register it
    if hasattr(cls, 'class_id'):
        LoggingDevice.child_classes[cls.class_id] = cls
    return cls  # Return the class object

class LoggingDevice():

    child_classes = {} #Dictionary containing all types of logging devices (their class references)
    class_id = "00" #Just to suppress warning
      
    def __init__(self, alias, interval, *args, **kwargs):
        self.id = self.__class__.class_id
        self.alias = alias
        self.interval = interval
        if (self.interval > 0):
            task_manager.add_task(self.alias, self.log, self.interval) # Run every self.interval seconds
        asyncio.create_task(self.handle())  #Intended to run continuously if there is such need for the LoggingDevice to work properly
        if logging_devices is not None:
            self.info = logging_devices[self.id]
        self.importDependancies() #TODO: fix this

    def log(self, message):
        dt = get_readable_time(rtc.datetime()[:7])
        logTuple = (self.alias, dt) + message
        
        print(f"{self.alias} logging: {str(logTuple)}")
        #Write Log Message to SD Card
        if config is not None:
            append_to_file(config["storage"]["log_file_path"], str(logTuple)+",")

    async def handle(self): #Will be run continuously in event loop if defined in child classes
        pass

    @classmethod
    def create_instance(cls, class_id, **kwargs):
        # Create instance of the child class based on the class_id
        if class_id in cls.child_classes:
            if logging_devices is not None:
                print((logging_devices[class_id]["constructor_arg_defaults"] | kwargs))
                return cls.child_classes[class_id](**(logging_devices[class_id]["constructor_arg_defaults"] | kwargs))
        else:
            raise ValueError(f"No child class registered with ID '{class_id}'")


    def importDependancies(self):
        for module in self.info["module_dependencies"]:
            #dynamic_import(module) #TODO: Fix this
            pass

@register_child
class DHT11_LoggingDevice(LoggingDevice):
    class_id = "01" #Hard coded id for DHT11 Sensor Logging Device (for Parent recognition)
    def __init__(self, alias, pin, interval, *args, **kwargs):
        
        super().__init__(alias, interval)
        self.sensor = dht.DHT11(machine.Pin(pin))
    
    def measurement(self):
        try:
            # Measure temperature and humidity
            self.sensor.measure()
            temperature = self.sensor.temperature()  # Get temperature in Celsius
            humidity = self.sensor.humidity()  # Get humidity percentage

            return (temperature, humidity)
            #print("DHT-11 Temperature: {}°C  Humidity: {}%".format(temperature, humidity))

        except Exception as e:
            log_exception(e, rtc.datetime(), msg="DHT-11 failed measurement")
            return None

    def log(self):
        measurement = self.measurement()
        if measurement is None: return
        super().log(measurement)

@register_child 
class MPU6050_LoggingDevice(LoggingDevice):
    class_id = "02"
    def __init__(self, alias, scl, sda, interval, *args, **kwargs):
        super().__init__(alias, interval)
        self.i2c = get_i2c_instance(1, scl, sda, freq=400000)
        self.sensor = MPU6050_Accelerometer(self.i2c)
    
    def log(self):
        try:
            acc_x, acc_y, acc_z = self.sensor.get_acceleration()
            super().log((acc_x, acc_y, acc_z))
        except Exception as e:
            log_exception(e, rtc.datetime(), msg="MPU6050 failed measurement")

@register_child
class Regenmesser_LoggingDevice(LoggingDevice):
    class_id = "03"
    def __init__(self, alias, interval, pin, mmPerPulse, *args, **kwargs):
        super().__init__(alias, interval)
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.interuptFlag = False
        self.mmPerPulse = mmPerPulse
        self.mmTotal = 0
        self.debounce_time = 0
        self.lastLog = get_readable_time(rtc.datetime()[:7])
        self.pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.callback)
    
    def callback(self, pin):
        if (time.ticks_ms()-self.debounce_time > 500):
            self.interuptFlag = True
            self.debounce_time = time.ticks_ms()
    
    async def handle(self):
        while True:
            if (self.interuptFlag):
                self.mmTotal += self.mmPerPulse
                print("Regenmesser detected")
                self.interuptFlag = False
            await asyncio.sleep_ms(800) #NOTE: This delay must be smaller, than it takes a bucket to fill and trip
    
    def log(self):
        super().log((self.lastLog, self.mmTotal))
        dtNew = get_readable_time(rtc.datetime()[:7])
        self.lastLog = dtNew
        self.mmTotal = 0

@register_child
class GenericDigitalPin_LoggingDevice(LoggingDevice): #NOTE: Used by raindrop, etc. sensors
    class_id = "04"
    def __init__(self, alias, interval, pin):
        super().__init__(alias, interval)
        self.debounce_time = 0
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)

    def log(self):
        super().log((self.pin.value()))

@register_child
class GenericAnalogPin_LoggingDevice(LoggingDevice): #NOTE: Used by Soil Temp. , inbuilt Pico Tmep. , etc. analog sensors
    class_id = "05"
    def __init__(self, alias, interval, pin): #Must be a pin that supports analog input (26, 27, 28) + 29 (VSYS)
        super().__init__(alias, interval)
        self.pin = ADC(Pin(pin))

    def log(self):
        return super().log((self.pin.read_u16()))

@register_child
class WindDirection_LoggingDeviceSerial(LoggingDevice):
    class_id = "20"
    def __init__(self, alias, bus, tx, rx, interval, pins, *args, **kwargs):
        super().__init__(alias, interval)
        self.uart = get_UART_instance(bus, {"tx": tx, "rx": rx})

        data = ""
        for key, value in pins.items(): #NOTE: Sorting of pin declarations in JSON file is IMPORTANT!
            data += value + ","
        data = data[:-1]
        self.uart.write("_setup\n"+self.id+","+self.alias+","+data+"\n") #Command \n data \n
        res = self.uart.readline() #NOTE: Dont know if newline is included in return value
        if (res != "OK"): #Check for succesful acknowledgement by arduino
            log_exception(OSError("Error while configuring Serial Logging Device"), datetime=rtc.datetime())

    def log(self):
        self.uart.write("_req\n"+self.alias+"\n")
        res = self.uart.readline()

myLoggingDevices = []

async def main():
    if config is not None:
        for device in config["loggingDevices"]:
            #print(device)
            myLoggingDevices.append(LoggingDevice.create_instance(device["id"], **(device["constructor_args"] | {'alias': device["alias"]})))

    while True:
        await task_manager.list_tasks()
        await asyncio.sleep(50)

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

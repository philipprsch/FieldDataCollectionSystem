import uasyncio as asyncio
import machine
import lib.sdcard as sdcard
import uos  # Use uos instead of os for MicroPython
from machine import RTC, I2C, Pin
import time
from task_manager import TaskManager
from helpers import read_json, dynamic_import, append_to_file, read_file, does_folder_exist, get_readable_time

#Only to supress error, should be dinamically imported
import dht 
from accelerometer import MPU6050_Accelerometer
#Read LoggingDevices file
logging_devices = read_json("lookup/LoggingDevices.json")
print(logging_devices)

config = read_json("config/config.json")
if config is None: OSError("No configuration file found")

rtc = RTC() #Use onbaord Pico RTC, can be replaced by external RTC Module

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
        self.importDependancies()

    def log(self, message):
        dt = get_readable_time(rtc.datetime()[:7])
        logTuple = (self.alias, dt) + message
        
        print(f"{self.alias} logging: {str(logTuple)}")
        #Write Log Message to SD Card
        if config is not None:
            append_to_file(config["storage"]["log_file_path"], str(logTuple)+",")

    async def handle(self): #Will be run continuously in event loop if defined
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

        except OSError as e:
            print("DHT-11 Failed to read sensor data: ", e)

    def log(self):
        measurement = self.measurement()
        if measurement is None: return
        super().log(measurement)

@register_child 
class MPU6050_LoggingDevice(LoggingDevice):
    class_id = "02"
    def __init__(self, alias, scl, sda, interval, *args, **kwargs):
        super().__init__(alias, interval)
        self.i2c = I2C(1, sda=Pin(sda), scl=Pin(scl), freq=400000)
        self.sensor = MPU6050_Accelerometer(self.i2c)
    
    def log(self):
        acc_x, acc_y, acc_z = self.sensor.get_acceleration()
        super().log((acc_x, acc_y, acc_z))

@register_child
class Regenmesser_LoggingDevice(LoggingDevice):
    class_id = "03"
    def __init__(self, alias, interval, pin, mmPerHigh, *args, **kwargs):
        super().__init__(alias, interval)
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.interuptFlag = False
        self.mmPerHigh = mmPerHigh #TODO: Rename to mmPerPulse
        self.mmTotal = 0
        self.debounce_time = 0
        self.lastLog = get_readable_time(rtc.datetime()[:7])
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.callback)
    
    def callback(self, pin):
        if (time.ticks_ms()-self.debounce_time > 500):
            self.interuptFlag = True
            self.debounce_time = time.ticks_ms()
    
    async def handle(self):
        while True:
            if (self.interuptFlag):
                self.mmTotal += self.mmPerHigh
                print("Regenmesser detected")
                self.interuptFlag = False
            await asyncio.sleep_ms(800) #NOTE: This delay must be smaller, than it takes a bucket to fill and trip
    
    def log(self):
        super().log((self.lastLog, self.mmTotal))
        dtNew = get_readable_time(rtc.datetime()[:7])
        self.lastLog = dtNew
        self.mmTotal = 0

myLoggingDevices = []

async def main():
    if config is not None:
        for device in config["loggingDevices"]:
            print(device)
            myLoggingDevices.append(LoggingDevice.create_instance(device["id"], **(device["constructor_args"] | {'alias': device["alias"]})))

    while True:
        await task_manager.list_tasks()
        await asyncio.sleep(50)

# Run the event loop
asyncio.run(main())

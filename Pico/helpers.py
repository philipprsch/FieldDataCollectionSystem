import ujson
import sys
import uos
from machine import Pin, I2C, UART
from defines import *
import time

def read_json(file_path):
    with open(file_path, 'r') as file:
        # Load and parse the JSON content into a Python dictionary
        data = ujson.load(file)
        return data
 
def is_module_imported(module_name):
    # Check if the module is already in sys.modules
    return module_name in sys.modules

def dynamic_import(module_name):
    # Dynamically import the module
    if is_module_imported(module_name):
        print(f"Module '{module_name}' is already imported.")
        return None
    try:
        module = __import__(module_name)
        print(f"Module '{module_name}' imported successfully.")
        return module
    except ImportError:
        print(f"Failed to import module '{module_name}'.")


#Helper functions for file manipulation
def does_folder_exist(directory):
    # Try listing the contents of the directory
    try:
        uos.listdir(directory)
        return True  
    except OSError:
        return False  

def ensureFileExistance(file_path): 
    try:
        uos.stat(file_path)
    except OSError as e:
        if e.args[0] == 2:  # ENOENT error code
            # File does not exist; create it
            with open(file_path, "w") as f:
                f.write("")

def append_to_file(filename, data):
    with open(filename, "a") as file:  # 'a' mode for appending
        file.write(data)
        #print(f"Data '{data}' appended to {filename}")
        print("DATA appended")

# Read from file
def read_file(filename): #NOTE: Check for OSError
    with open(filename, "r") as file:
        content = file.read()
        #print(f"Contents of {filename}:")
        #print(content)
        return content    

#Time functions

def get_readable_time(datetime_tuple):
    if len(datetime_tuple) == 7:
        year, month, day, weekday, hours, minutes, seconds = datetime_tuple
    elif len(datetime_tuple) == 8:
        year, month, day, weekday, hours, minutes, seconds, s = datetime_tuple

    # Format time
    return f"{day:02d}/{month:02d}/{day:02d} {hours:02d}:{minutes:02d}:{seconds:02d}"
    #return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"


#Only make one I2C insatnce per bus
_i2c_instances = {}

class I2CInstancePins(Exception):
    def __init__(self, bus, scl, sda, scl_new, sda_new):
        self.message = f"Pins scl={scl_new}, sda={sda_new} do not match existing I2C instance for bus={bus} with scl={scl}, sda={sda}"
        super().__init__(self.message)


def get_i2c_instance(bus, scl_pin=None, sda_pin=None, **kwargs):
    global _i2c_instances
    if bus is None: raise ValueError("Bus must be specified")
    # Define default pins for each bus (for Raspberry Pi Pico)
    default_pins = {
        0: {'scl': 21, 'sda': 20},  # I2C0 default pins on the Pico (GP21=SCL, GP20=SDA)
        1: {'scl': 27, 'sda': 26},  # I2C1 default pins on the Pico (GP27=SCL, GP26=SDA)
    }
    
    # Check if the instance for the requested bus already exists
    if bus in _i2c_instances:
        #Check if an object using the sam bus but other pins has already been initialized
        if (scl_pin != _i2c_instances[bus]["scl_pin"] or sda_pin != _i2c_instances[bus]["sda_pin"]):
            raise I2CInstancePins(bus, _i2c_instances[bus]["scl_pin"], _i2c_instances[bus]["sda_pin"], scl_pin, sda_pin)
        return _i2c_instances[bus]["obj"]
    
    # Use default pins if none are provided
    if scl_pin is None:
        scl_pin = default_pins[bus]['scl']
    if sda_pin is None:
        sda_pin = default_pins[bus]['sda']
    
    # Create a new I2C instance for the bus and store it in the dictionary
    _i2c_instances[bus] = {
        "scl_pin": scl_pin,
        "sda_pin": sda_pin,
        "obj": I2C(bus, scl=Pin(scl_pin), sda=Pin(sda_pin), **(I2C_DEFAULT_PARAMETERS | kwargs))  # Create a new I2C instance for the bus and store it in the dictionary
    }
    
    return _i2c_instances[bus]["obj"]

_UART_instances = {}

class UARTInstancePins(Exception):
    def __init__(self, bus, tx, rx, tx_new, rx_new):
        self.message = f"Pins tx={tx_new}, rx={rx_new} do not match existing UART instance for bus={bus} with tx={tx}, rx={rx}"
        super().__init__(self.message)


def get_UART_instance(bus, tx_pin=None, rx_pin=None, **kwargs): #Kwargs may include Bits, Parity, Stop
    global _UART_instances
    if bus is None: raise ValueError("Bus must be specified")

    print(kwargs)
    print(tx_pin)
    print(rx_pin)

    if (bus in _UART_instances):
        #Check if pins are provided and if they maatch pins of current instance
        if (tx_pin!= _UART_instances[bus]["tx_pin"] or rx_pin!= _UART_instances[bus]["rx_pin"]):
            raise UARTInstancePins(bus, _UART_instances[bus]["tx_pin"], _UART_instances[bus]["rx_pin"], tx_pin, rx_pin)
        # Return existing instance
        return _UART_instances[bus]["obj"]
    default_pins = {
        0: {'tx': 0, 'rx': 1}, 
        1: {'tx': 4, 'rx': 5}
    }
    if tx_pin is None:
        tx_pin = default_pins[bus]['tx']
    if rx_pin is None:
        rx_pin = default_pins[bus]['rx']
    _UART_instances[bus] = {
        "tx_pin": tx_pin,
        "rx_pin": rx_pin,
        "obj": UART(bus, tx=Pin(tx_pin), rx=Pin(rx_pin), **( UART_DEFAULT_PARAMETERS | kwargs))
    }   
    return _UART_instances[bus]["obj"]
        
def waitForRespnese(uart, timeout):
    start_time = time.ticks_ms()
    
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
        if uart.any():  # Check if data is available in the UART buffer
            return True
        time.sleep_ms(2)  # Small delay to reduce CPU usage
    
    return False

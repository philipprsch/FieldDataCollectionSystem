import ujson
import sys
import uos
from machine import Pin, I2C, UART

def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            # Load and parse the JSON content into a Python dictionary
            data = ujson.load(file)
            return data
    except OSError as e:
        print(f"Error opening file: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return None
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
    
def append_to_file(filename, data):
    with open(filename, "a") as file:  # 'a' mode for appending
        file.write(data)
        #print(f"Data '{data}' appended to {filename}")
        print("DATA appended")

# Read from file
def read_file(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
            print(f"Contents of {filename}:")
            print(content)
            return content
    except OSError:
        print(f"{filename} does not exist yet.")
        return ""

#Time functions

def get_readable_time(datetime_tuple):
    year, month, day, weekday, hours, minutes, seconds = datetime_tuple

    # Format time
    return f"{day:02d}/{month:02d}/{day:02d} {hours:02d}:{minutes:02d}:{seconds:02d}"
    #return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"


#Only make one I2C insatnce per bus
_i2c_instances = {}

def get_i2c_instance(bus=0, scl_pin=None, sda_pin=None, freq=400000):
    global _i2c_instances
    
    # Define default pins for each bus (for Raspberry Pi Pico)
    default_pins = {
        0: {'scl': 21, 'sda': 20},  # I2C0 default pins on the Pico (GP21=SCL, GP20=SDA)
        1: {'scl': 27, 'sda': 26},  # I2C1 default pins on the Pico (GP27=SCL, GP26=SDA)
    }
    
    # Check if the instance for the requested bus already exists
    if bus in _i2c_instances:
            #NOTE: Here one could check if an object using the sam bus but other pins has already been initialized
            return _i2c_instances[bus]
    
    # Use default pins if none are provided
    if scl_pin is None:
        scl_pin = default_pins[bus]['scl']
    if sda_pin is None:
        sda_pin = default_pins[bus]['sda']
    
    # Create a new I2C instance for the bus and store it in the dictionary
    _i2c_instances[bus] = I2C(bus, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
    
    return _i2c_instances[bus]

_UART_instances = {}

UART_BAUDRATE = 9600
UART_TIMEOUT = 2000

def get_UART_instance(id, *args, **kwargs): #Kwargs may include Bits, Parity, Stop
    if (id in _UART_instances):
        return _UART_instances[id]
    default_pins = {
        0: {'tx': 0, 'rx': 1}, 
        1: {'tx': 4, 'rx': 5}
    }
    _UART_instances[id] = UART(baudrate=UART_BAUDRATE)
    _UART_instances[id].init(id, **( {"bits":8, "parity":None, "stop":1, "timeout": UART_TIMEOUT} | default_pins[id] | kwargs))
    return _UART_instances[id]
        

#Exception handeling
import traceback

# Define a function to log errors to a file
MAX_LOG_SIZE = 1024 * 1024  # 1 MB

from main import rtc

def log_exception(e, msg=None):
    try:
        datetime = get_readable_time(rtc.datetime())
    except Exception as e2:
        datetime = "TIME UNKNOWN"

    if (msg is not None): print(msg)
    print(f"Exception: {str(e)} was logged to file")

    log_file = '/error_log.txt'
    
    # Check the size of the log file
    if uos.stat(log_file)[6] > MAX_LOG_SIZE:
        uos.rename(log_file, '/error_log_old.txt')  # Archive the old log

    try:
        with open(log_file, 'a') as f:
            f.write('--- Exception occurred on {} ---\n'.format(datetime))
            if msg: f.write(msg + '\n')
            f.write(str(e) + '\n')
            f.write(traceback.format_exc() + '\n')
            f.write('\n')
    except Exception as log_error:
        print("Failed to log exception:", log_error)
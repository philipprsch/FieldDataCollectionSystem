import machine
import lib.sdcard as sdcard

import uos  # Use uos instead of os for MicroPython

# Initialize SPI and SD card
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
uos.mount(vfs, "/sd")

# File operations
file_path = "/sd/data.txt"

# Create (if not existent) and append data to file
def append_to_file(filename, data):
    with open(filename, "a") as file:  # 'a' mode for appending
        file.write(data + "\n")
        print(f"Data '{data}' appended to {filename}")

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

# Example usage
append_to_file(file_path, "Hello, World!")
append_to_file(file_path, "Data written to SD card.")
read_file(file_path)

# Unmount the SD card after use
uos.umount("/sd")

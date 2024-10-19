import machine
import ubluetooth
from machine import Timer

class BluetoothServer:
    def __init__(self):
        self.ble = ubluetooth.BLE()
        self.ble.active(False)
        self.connected = False
        self.ble.irq(self.bt_irq)
        self.tx = None  # TX characteristic for sending data

        # BLE service UUID and characteristics (UART service simulation)
        UART_SERVICE_UUID = ubluetooth.UUID(0x1812)
        UART_TX_CHAR_UUID = ubluetooth.UUID(0x2A99)
        UART_RX_CHAR_UUID = ubluetooth.UUID(0x2A98)
        
        self.tx = (UART_TX_CHAR_UUID, ubluetooth.FLAG_NOTIFY)
        self.rx = (UART_RX_CHAR_UUID, ubluetooth.FLAG_WRITE)

        self.services = [(UART_SERVICE_UUID, (self.tx, self.rx))]
        self.ble.config(gap_name="PicoW-BT-Time")
    
    def bt_irq(self, event, data):
        if event == 1:  # A central connected
            print("Device connected")
            self.connected = True
        elif event == 2:  # A central disconnected
            print("Device disconnected")
            self.connected = False
        elif event == 3:  # A write event, meaning data is received
            buffer = self.ble.gatts_read(self.rx_handle)
            print(f"Received data: {buffer.decode('utf-8')}")

    def start_advertising(self):
        self.ble.gap_advertise(100, b'\x02\x01\x06' + b'\x03\x03\xD0\x18')
        print("Bluetooth advertising started...")

    def stop_advertising(self):
        self.ble.gap_advertise(None)
        print("Bluetooth advertising stopped")

    def enable(self):
        self.ble.active(True)
        ((self.tx_handle, self.rx_handle),) = self.ble.gatts_register_services(self.services)
        self.start_advertising()

    def disable(self):
        self.ble.active(False)
        print("Bluetooth disabled")

# Callback function for button press interrupt
def button_handler(pin):
    print("Button pressed, enabling Bluetooth...")
    bluetooth_server.enable()

# Set up the button on GPIO 10 with an interrupt
button = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_DOWN)
button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)

# Initialize the Bluetooth server
bluetooth_server = BluetoothServer()

# Timer to periodically check for connection status and close connection
def check_bluetooth_status(t):
    if bluetooth_server.connected:
        # Assume here we want to request the time once connected
        print("Requesting time from device...")
        # Write a message to the central device requesting the time
        bluetooth_server.ble.gatts_notify(bluetooth_server.tx_handle, b"Send Time")

        # In a real scenario, you would wait for the device to respond with time
        # and handle it in the bt_irq() function when data is received.

        # Simulate closing the connection after receiving the time
        bluetooth_server.disable()

# Set up a timer to check Bluetooth status every second (non-blocking)
status_timer = Timer()
status_timer.init(period=1000, mode=Timer.PERIODIC, callback=check_bluetooth_status)

# The main loop is event-driven now, with no blocking code.
# The button press is handled via interrupts, and Bluetooth events are managed asynchronously.

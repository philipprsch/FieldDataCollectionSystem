import machine
import time
import dht

class DH11:
  def __init__(self, name, age):
    self.name = name
    self.age = age
# Initialize DHT11 sensor (GPIO 22)
sensor = dht.DHT11(machine.Pin(22))

while True:
    try:
        # Measure temperature and humidity
        sensor.measure()
        temperature = sensor.temperature()  # Get temperature in Celsius
        humidity = sensor.humidity()  # Get humidity percentage

        # Print the results
        print("Temperature: {}°C  Humidity: {}%".format(temperature, humidity))

    except OSError as e:
        print("Failed to read sensor data: ", e)

    # Wait for a few seconds before the next reading
    time.sleep(2)

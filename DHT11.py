import machine
import time
import dht


sensor = dht.DHT11(machine.Pin(10))

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

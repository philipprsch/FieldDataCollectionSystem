# Asynchronous Sensor Logging System

This system is designed to periodically and asynchronously gather sensor data from various logging devices (sensors) at custom, individually set intervals. The logged data is saved onto an SD card for (optional) further processing or analysis. All configuration parameters are customizable and stored in a JSON configuration file.

## Table of Contents
- [Configuration](#configuration)
- [Logging Devices](#logging-devices)
  - [Parameters](#parameters)
  - [Example](#example)
- [Device Lookup](#device-lookup)
- [SD Card Logging](#sd-card-logging)

---

## Configuration

The system's configuration is managed through a `config.json` file, which stores all the parameters required for the devices to operate. The configuration file can be found in the following path: config/config.json

This file can be manually edited to change logging device settings such as IDs, aliases, and intervals for sensor data collection.

## Logging Devices

In the `LoggingDevices` array, you can add one or more logging devices (usually sensors) that will be read at specified intervals. Each device has a set of parameters that define how it operates and interacts with the system.

### Parameters

- **`id`** (*required*):
  - Specifies the class that the device uses within the code.
  - A list of all acceptable IDs and their corresponding devices or sensors can be found in `lookup/LoggingDevices.json`.
  - For example, the ID `"01"` is reserved for a DHT-11 sensor.
  - Some IDs, like `"03"` or `"04"`, can be used for multiple devices that either use a digital or analog pin, respectively.
  - Note that an `id` does not uniquely identify a device, as one could have multiple (similar or even identical) 
devices that use the same class and thus also `id`. Unique identification is achieved though `alias`.

- **`alias`** (*required*):
  - A user-defined string that uniquely identifies the logging device and is included in its log messages.
  - This alias is arbitrary and can be any string the user chooses (e.g., "Room1_DHT11").

- **`info`** (optional):
  - Additional user-defined information to help identify the device (e.g., mounting location, purpose, etc.).

- **`constructor_args`** (*required*):
  - Specifies the configuration parameters required to initialize the device.
  - Each device has a set of default parameters defined in `lookup/LoggingDevices.json`.
  - One common parameter is `interval`, which determines how frequently the device logs its data to the SD card.
    - **Interval of `0`**: Disables periodic logging for that device (e.g., when data is logged based on external triggers).
  - Other parameters (e.g. sda, scl, pin) are used to specify how the device is connected to the Pico

### Example

Here's an example of how a logging device might be configured in `config/config.json`:

```json
{
    "LoggingDevices": [
        {
            "id": "01",
            "alias": "Room1_DHT11",
            "info": "Living Room Temperature Sensor",
            "constructor_args": {
                "interval": 600,
                "pin": 5
            }
        },
        {
            "id": "03",
            "alias": "Garden_Moisture",
            "info": "Garden Soil Moisture Sensor",
            "constructor_args": {
                "interval": 300,
                "pin": 16
            }
        }
    ]
}
```
---
### SD Card Logging
---
All devices in the configuration file log onto the SD-Card.
The file path to the log-file can be set in the `config/config.json` file under `storage -> log_file_path`
This system serves the main pupose of perodically and asynchronously gathering sensor (logging device) data at custom and
individually set intervals, which is saved onto an SD-Card.

All the configuration parameters are stored and can be manually changed in the config/config.json file
In the LoggingDevices array field, one can add so called "Logging Devices" which usually are sensors.
Each Logging Device has the following parameters:

"id" (*) - The id specifies which class in the code this device uses.
A list of all accaptable id's, along with a description of the sensor that corresponds to this id or
the type of devices that are meant to be used with this id/class, can be found in the lookup/LoggingDevices.json file

For instance the id "01" (note that ids are strings of two digits) is specifically reserved for a DHT-11 sensor.
Id's "03" and "04" on the other hand may be used by used by multiple sensors, as long as they simply require
a digital or analoge pin to be read respectively.

Note that an id does not uniquely identify a device, as one could have multiple (similar or even identical) 
devices that use the same class and thus also id. Unique identification is achieved though aliases.

"alias" (*) - An arbitrary user-set string that will be included in the logging messages this device produces. 
            Does not have a specific dictated format. 

"info" - Can be set by the user to easily identify the device (e.g. mounting location, etc.)

"constructor_args" (*) - All devices rely on additional configuration parameters for initialization. A list of the default
                        parameters for each device can be found in lookup/LoggingDevices.json. A parameter all devices
                        share is "interval". "Interval" specifies the frequency at which the device will save its readings
                        to the SD-Card. For some (simple) sensors this is also the rate at which readings are taken, though other
                        devices may be collecting and processing readings in the background. "interval" may also be set to 0 to
                        disable data logging if for instance the device logs data at other (non-periodic) occasions.

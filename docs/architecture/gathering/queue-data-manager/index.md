---
layout: doc-entry
title:  "Queue and Data Manager"
---

In order to exchange data between the twe seperate threads, the system uses the data_manager and queue_manager interfaces.
These are described in more detail here.


# Table of Contents
[Data Manager](#data-manager)

[Queue Manager](#queue-manager)

______________
# Data Manager
The data manager provides the last recorded values from the gathering backend.
If in the current runtime no gathering of the requested resource has been done, the data_manager will return None.

### Get the last saved measurement

    def getMeasurement(component, metric, args=None):

Example:
```
import data_manager
lastData = data_manager.getMeasurement("cpu","usage")
print(lastData) # Will print the latest CPU Usage if it was already recorded
```

### Set a new measurement

    def setMeasurement(component, metric, value, args=None):

Example:
```
import data_manager
import time
newMeasurement = {
    "timestamp" : time.time() / 1000 # Divide by 1000 to get millisecond timestamp
    "value" : 50
    }
data_manager.setMeasurement("cpu", "usage", newMeasurement)
```

_______________
# Queue Manager
The Queue Manager is also a way to get measurement values however it also provides methods to send data requests to the gathering side and the implementation is quite different.
See: https://docs.python.org/3/library/asyncio-queue.html

The system relies on Python's queue module which is quite useful if real-time data is being sent to the client via Websockets or something similar.
It is not advised to directly access the queues. Rather the following methods should be used.

### Read a measurement from the queue

    def readMeasurementFromQueue(component, metric, args=None):

Arguments:
- See Components & Metrics page

### Put a measurement into the queue

    def putMeasurementIntoQueue(component, metric, measurement, args=None):

Arguments:
- See Components & Metrics page
- measurement: A dictionary containing "timestamp" (milliseconds since Unix Epoch) and "value" (varies across metric)

```
import queue_manager
import time
newMeasurement = {
    "timestamp" : time.time() / 1000 # Divide by 1000 to get millisecond timestamp
    "value" : 50
    }
queue_manager.putMeasurementIntoQueue("cpu", "usage", newMeasurement) # Puts a cpu usage into the queue with the value 50
```

### Send a single new data request

    def requestData(component, metric, args=None):

Arguments:
- See Components & Metrics page

This queue is used to request immediate new data from the backend. Think of it like a refresh button the user clicked.
Please remember, that this function only requests new data. It returns nothing.
After using this function the program has to wait for the new data to be updated within the data_manager or in the queue_manager.
Also if you want to get repeatedly new data, use the setGateringRate function.

```
import queue_manager
queue_manager.requestData("cpu","usage") # Requests an updated measurement to be put into data_manager, queue_manager and the database
```

### Set the gathering rate of the specified component/metric

    def setGatheringRate(component, metric, delayms, args=None):

Arguments:
- See Components & Metrics page
- delayms: This specifies the time in milliseconds between measurements. E.g. a value of 1000 will take a measurement every second. Also note that a zero will disable the rate gathering.

Example:
```
import queue_manager
queue_manager.setGatheringRate("cpu", "usage", 1000) # Creates a gatherer in the backend, that records the cpu usage every second
```
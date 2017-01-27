import os
from pynvml import nvmlInit, NVMLError, nvmlSystemGetDriverVersion, \
                   nvmlDeviceGetName, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex

try:
    nvmlInit()
    print("Driver Version:", nvmlSystemGetDriverVersion())
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        print("Device", i, ":", nvmlDeviceGetName(handle))

except NVMLError as err:
    print("Failed to initialize NVML: ", err)
    print("Exiting...")

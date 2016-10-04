import os
from pynvml import nvmlInit, NVMLError

try:
    nvmlInit()
except NVMLError as err:
    print("Failed to initialize NVML: ", err)
    print("Exiting...")
    os._exit(1)
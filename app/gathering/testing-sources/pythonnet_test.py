import sys
import time
import os
import atexit

# sys.path.append("C:/Users/Alex/Dropbox/Schule/Semester 5/Studienarbeit 2/Source/opserv-backend/app/gathering/testing-sources")
sys.path.append("C:/Users/Lucas/PycharmProjects/opserv-backend/app/extern_dependency")

# sys.path.append(os.path.dirname(__file__))

typeList = [
    "Voltage",
    "Clock",  # MHz
    "Temperature",  # °C
    "Load",  # %
    "Fan",  # RPM
    "Flow",  # L/h
    "Control",  # %
    "Level",  # %
    "Factor",  # 1
    "Power",  # W
    "Data",  # GB = 2^30 Bytes
]

tempList = []


def hardwareAdded(hardware):
    print(hardware.Name)
    print(hardware.GetReport())
    for sensor in hardware.Sensors:
        print(typeList[sensor.SensorType])
        print(sensor.Name, sensor.Value)
        if typeList[sensor.SensorType] == "Temperature":
            tempList.append([hardware, sensor])
        for val in sensor.Values:
            print(val)
    for hw in hardware.SubHardware:
        hardwareAdded(hw)


import clr

clr.AddReference("OpenHardwareMonitorLib")

from OpenHardwareMonitor import Hardware

print(Hardware.Computer())

pc = Hardware.Computer()
pc.MotherboardEnabled = True
pc.RAMEnabled = True
pc.GPUEnabled = True
pc.CPUEnabled = True
pc.HDDEnabled = True
pc.HardwareAdded += hardwareAdded
pc.HardwareRemoved += hardwareAdded
print(pc.GetReport())
pc.Open()


def closingHandler():
    pc.Close()
    print("closed that ho")


atexit.register(closingHandler)

print("SUCCEED")
startTime = time.time()
while True:
    time.sleep(0.5)
    for s in tempList:
        s[0].Update()
        print(s[1].Name, s[1].Value)
    if time.time() - startTime > 2:
        break

pc.Close()

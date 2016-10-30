#
# Handles the connection to and provides a simple interface to the OpenHardwareMonitorLib
#
# Warning, this module is highly experimental and can result in unpredictable behaviour
# Also it needs the OpenMonitorHardwareLib.dll in the dependency folder
# For a more detailed code example check the OpenHardwareMonitor GitHub Repository
#
# 05.10.2016
#
# Usage: 
#

import logging

import clr

log = logging.getLogger("opserv.gathering.measure.ohm")
log.setLevel(logging.DEBUG)

ohm_ready = False
pc = None
hardwareList = []

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


def init():
    # Load Assembly
    clr.AddReference("OpenHardwareMonitorLib")

    # Import necessary Classes
    from OpenHardwareMonitor import Hardware

    # Create Computer Instance for the current system
    pc = Hardware.Computer()

    # Enable gathering from the specified sources
    pc.MotherboardEnabled = False
    pc.FanControllerEnabled = False
    pc.RAMEnabled = True
    pc.GPUEnabled = True
    pc.CPUEnabled = True
    pc.HDDEnabled = True
    # Open the PC Connection (inserting driver into system)
    try:
        pc.Open()
    except Exception as e:
        log.error(e)
        log.error("Could not open OHM Driver Connection. Does the app have Administrator rights?")
        # OpenHardwareMonitorLib connection ready


def deinit():
    pc.Close()

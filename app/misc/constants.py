#
# Constant declarations that are centralized here
#
# 27.09.2016
#
# Example usage:
#
# from misc.constants import implemented_hardware
#
# print(implemented_hardware)
#

from enum import Enum

cpu_metrics = {
    "usage",
    "temperature",
    "info",
    "frequency"
}

gpu_metrics = {
    "info",
    "gpuclock",
    "memclock",
    "vramusage",
    "temperature",
    "usage"
}

core_metrics = {
    "info",
    "frequency",
    "usage",
    "temperature"
}

memory_metrics = {
    "total",
    "free",
    "used"
}

process_metrics = {
    "cpuusage",
    "memusage",
    "name"
}

partition_metrics = {
    "total",
    "free",
    "used"
}

disk_metrics = {
    "temperature",
    "usage",
    "status"
}

network_metrics = {
    "info",
    "receivepersec",
    "transmitpersec"
}

system_metrics = {
    "cpus",
    "gpus",
    "cores",
    "partitions",
    "processes",
    "networks",
    "disks"
}

implemented_hardware = {
    "cpu": cpu_metrics,
    "gpu": gpu_metrics,
    "memory": memory_metrics,
    "disk": disk_metrics,
    "partition": partition_metrics,
    "process": process_metrics,
    "network": network_metrics,
    "system": system_metrics
}

default_gathering_rates = {
    "system": {
        "default": {
            ("cpus", 300000),
            ("gpus", 300000),
            ("cores", 300000),
            ("partitions", 300000),
            ("processes", 300000),
            ("networks", 300000),
            ("disks", 300000)
        }
    },
    "cpu": {
        "0": {
            ("usage", 60000),
            ("temperature", 60000),
            ("info", 60000),
            ("frequency", 60000)
        }
    }
}

# This describes the default values aswell as whether specific hardware requires additional argument information
# The tuple has this structure: (ARGUMENTNECESSARY, DEFAULTVALUE)
HARDWARE_DEFAULTS = {
    "cpu": (True, 0),
    "gpu": (True, 0),
    "core": (True, 0),
    "memory": (False, None),
    "disk": (True, None),
    "partition": (True, None),
    "process": (True, None),
    "system": (False, None),
    "network": (True, None)
}

Operating_System = Enum("Operating_System", "windows linux macos freebsd")
GraphicsVendor = Enum("GraphicsVendor", "intel nvidia amd")
CpuVendor = Enum("CpuVendor", "intel amd")


GATHERING_QUEUELISTENER_DELAY = 0.05 # Delay between the queueListener calls in the gathering thread (in seconds)

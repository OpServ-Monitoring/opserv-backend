"""#
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
"""
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
    "cores",
    "gpus",
    "cores",  # TODO double entry?
    "partitions",
    "processes",
    "networks",
    "disks"
}

implemented_hardware = {
    "cpu": cpu_metrics,
    "core": core_metrics,
    "gpu": gpu_metrics,
    "memory": memory_metrics,
    "disk": disk_metrics,
    "partition": partition_metrics,
    "process": process_metrics,
    "network": network_metrics,
    "system": system_metrics
}

# Map System metrics onto the regular components
SYSTEM_METRICS_TO_COMPS = {
    "cpus" : "cpu",
    "cores" : "core",
    "gpus" : "gpu",
    "partitions" : "partition",
    "processes" : "process",
    "networks" : "network",
    "disks" : "disk"
}

default_gathering_rates = {
    "system": {
        None: {
            # every 5 minutes
            ("cpus", 300000),
            ("gpus", 300000),
            ("cores", 300000),
            ("partitions", 300000),
            ("processes", 300000),  # TODO Increase rate
            ("networks", 300000),  # TODO Increase rate
            ("disks", 300000)
        }
    },
    "cpu": {
        "0": {
            ("usage", 60000),  # every minute
            ("temperature", 60000),  # every minute
            ("info", 300000),  # every 5 minutes
            ("frequency", 60000)  # every minute
        }
    },
    "memory": {
        None: {
            ("total", 300000),  # every 5 minutes
            ("free", 60000),  # every minute
            ("used", 60000)  # every minute
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

GATHERING_QUEUELISTENER_DELAY = 0.05  # Delay between the queueListener calls in the gathering thread (in seconds)

QUEUEMANAGER_DEFAULT_TIMEOUT = 2

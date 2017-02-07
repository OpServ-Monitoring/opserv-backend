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
import logging
from os.path import join

from misc.standalone_helper import get_path_to_app



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
    "cpucores",
    "gpus",
    "partitions",
    "processes",
    "networks",
    "disks"
}

implemented_hardware = {
    "cpu": cpu_metrics,
    "cpucore": core_metrics,
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
    "cpus": "cpu",
    "cpucores": "cpucore",
    "gpus": "gpu",
    "partitions": "partition",
    "processes": "process",
    "networks": "network",
    "disks": "disk"
}

def COMPS_TO_SYSTEM_METRICS(comp):
    for key, value in SYSTEM_METRICS_TO_COMPS.items():
        if value == comp:
            return key
    return None

default_gathering_rates = {
    "system": {
        None: {
            # every 5 minutes
            ("cpus", 300000),
            ("gpus", 300000),
            ("cpucores", 300000),
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
    "cpucore": (True, 0),
    "memory": (False, None),
    "disk": (True, None),
    "partition": (True, None),
    "process": (True, None),
    "system": (False, None),
    "network": (True, None)
}


def component_needs_arg(component_type):
    if component_type not in HARDWARE_DEFAULTS:
        # TODO Log error, component not found
        return False

    return HARDWARE_DEFAULTS[component_type][0]


# Enums are basically classes and not constats, the pylint warning is unnecessary
Operating_System = Enum("Operating_System", "windows linux macos freebsd")  # pylint: disable=C0103
GraphicsVendor = Enum("GraphicsVendor", "intel nvidia amd")  # pylint: disable=C0103
CpuVendor = Enum("CpuVendor", "intel amd")  # pylint: disable=C0103

GATHERING_QUEUELISTENER_DELAY = 0.05  # Delay between the queueListener
# calls in the gathering thread (in seconds)

QUEUEMANAGER_DEFAULT_TIMEOUT = 2  # seconds

MINIMUM_GATHERING_RATE = 500  # milliseconds

GATHERING_PERFORMANCE_LOG_DELAY = 2  # seconds

GATHERING_LOOP_SLEEP = 0.001 # seconds

DEFAULT_APP_CONFIG = {
    "port" : "31337",
    "cl" : logging.ERROR,
    "filelog" : join(get_path_to_app(), "opserv.log"),
    "log_usage" : False,
}

YES_PHRASES = ["y", "yes"] 
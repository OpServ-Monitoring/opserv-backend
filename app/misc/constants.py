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


cpu_valueTypes = {
    "usage",
    "temperature",
    "info",
    "frequency"
}

gpu_valueTypes = {
    "info",
    "gpuclock",
    "memclock",
    "vramusage",
    "temperature",
    "usage"
}

core_valueTypes = {
    "info",
    "frequency",
    "usage",
    "temperature"
}

memory_valueTypes = {
    "total",
    "free",
    "used"
}

process_valueTypes = {
    "cpuusage",
    "memusage",
    "name"
}

partition_valueTypes = {
    "total",
    "free",
    "used"
}

disk_valueTypes = {
    "temperature",
    "usage",
    "status"
}

network_valueTypes = {
    "info",
    "receivepersec",
    "transmitpersec"
}

system_valueTypes = {
    "cpus",
    "gpus",
    "cores",
    "partitions",
    "processes",
    "networks",
    "disks"
}


implemented_hardware = {
    "cpu": cpu_valueTypes,
    "gpu": gpu_valueTypes,
    "memory": memory_valueTypes,
    "disk": disk_valueTypes,
    "partition": partition_valueTypes,
    "process": process_valueTypes,
    "network": network_valueTypes,
    "system": system_valueTypes
}

# This describes the default values aswell as whether specific hardware requires additional argument information
# The tuple has this structure: (ARGUMENTNECESSARY, DEFAULTVALUE)
HARDWARE_DEFAULTS = {
    "cpu": (True, 0),
    "gpu": (True, 0),
    "memory": (False, None),
    "disk": (True, None),
    "partition": (True, None),
    "process": (True, None),
    "system": (False, None),
    "network": (True, None)
}
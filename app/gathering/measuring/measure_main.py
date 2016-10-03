#
# Main file for the different hardware and valueType measure methods
#
# 27.09.2016
#
#

import logging

from misc.helper import importIfExists

log = logging.getLogger("opserv.gatheringmeasure")
log.setLevel(logging.DEBUG)


# Optional depency importing
psutil = importIfExists("psutil")
pynvml = importIfExists("pynvml")
pyspectator = importIfExists("pyspectator")
cpuinfo = importIfExists("cpuinfo")

NOTIMPLEMENTED_NUMERICAL = 0
NOTIMPLEMENTED_TEXT = ""


def measure_cpu(valueType, args):
    if valueType == "usage":
        if psutil:
            return psutil.cpu_percent()
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "frequency":
        if cpuinfo:
            return cpuinfo.get_cpu_info()["hz_actual_raw"][0]
        return NOTIMPLEMENTED_NUMERICAL

    elif valueType == "info":
        if cpuinfo:
            return cpuinfo.get_cpu_info()["brand"]
        return NOTIMPLEMENTED_TEXT

    elif valueType == "temperature":
        if pyspectator:
            try:
                c = pyspectator.processor.Cpu(monitoring_latency=0.5)
                return c.temperature
            except Exception as e:
                log.error(e)

        return NOTIMPLEMENTED_NUMERICAL

def measure_core(valueType, args):
    
    if valueType == "info":
        if cpuinfo:
            return cpuinfo.brand
    elif valueType == "frequency":
        if cpuinfo:
            return cpuinfo.get_cpu_info()["hz_actual_raw"][0]
    elif valueType == "usage":
        if psutil:
            psutil.cpu_percent(percpu=True)[args]
    elif valueType == "temperature":
        return NOTIMPLEMENTED_NUMERICAL
def measure_gpu(valueType, args):
    if valueType == "info":
        return NOTIMPLEMENTED_TEXT
    elif valueType == "gpuclock":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "memclock":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "vramusage":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "temperature":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "usage":
        return NOTIMPLEMENTED_NUMERICAL

def measure_memory(valueType, args):
    if valueType == "total":
        return psutil.virtual_memory().total
    elif valueType == "free":
        return psutil.virtual_memory().available
    elif valueType == "used":
        return psutil.virtual_memory().used

def measure_process(valueType, args):
    if valueType == "cpuusage":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "memusage":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "name":
        return NOTIMPLEMENTED_TEXT

def measure_partition(valueType, args):
    if valueType == "totalspace":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "freespace":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "usedspace":
        return NOTIMPLEMENTED_NUMERICAL
    
def measure_disk(valueType, args):
    if valueType == "temperature":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "status":
        return NOTIMPLEMENTED_NUMERICAL


def measure_network(valueType, args):
    if valueType == "info":
        return NOTIMPLEMENTED_TEXT
    elif valueType == "receivepersec":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "transmitpersec":
        return NOTIMPLEMENTED_NUMERICAL

def get_system_data(valueType):
    if valueType == "cpus":
        return 1
    if valueType == "cores":
        return psutil.cpu_count()
    if valueType == "gpus":
        return 1
    if valueType == "disks":
        return NOTIMPLEMENTED_TEXT
    if valueType == "partitions":
        return str(psutil.disk_partitions())
    if valueType == "processes":
        return str(psutil.pids())
    if valueType == "networks":
        return str(getNetworkInterfaces())


def getNetworkInterfaces():
    ''' Gets the names of all currently available network interfaces and returns them in an array '''
    if not psutil:
        return []
    detailed_interfaces = psutil.net_if_stats()
    simple_interfaces = []
    for interface in detailed_interfaces:
        simple_interfaces.append(interface)
    return simple_interfaces
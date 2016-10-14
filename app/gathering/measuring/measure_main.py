#
# Main file for the different component and metric measure methods
#
# 27.09.2016
#
#

import logging
import sys

from misc.constants import Operating_System
from misc.helper import importIfExists

log = logging.getLogger("opserv.gathering.measure")
log.setLevel(logging.DEBUG)

log.debug("Logger for Measuremain started")

# Optional depency importing
psutil = importIfExists("psutil")
pynvml = importIfExists("pynvml")
pyspectator = importIfExists("pyspectator")
cpuinfo = importIfExists("cpuinfo")
clr = importIfExists("clr")


NOTIMPLEMENTED_NUMERICAL = 0
NOTIMPLEMENTED_TEXT = ""


def measure_cpu(metric, args):
    log.info("Retrieving cpu data")

    if metric == "usage":
        if psutil:
            return psutil.cpu_percent()
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "frequency":
        if cpuinfo:
            return cpuinfo.get_cpu_info()["hz_actual_raw"][0]
        return NOTIMPLEMENTED_NUMERICAL

    elif metric == "info":
        if cpuinfo:
            return cpuinfo.get_cpu_info()["brand"]
        return NOTIMPLEMENTED_TEXT

    elif metric == "temperature":
        if pyspectator:
            try:
                c = pyspectator.processor.Cpu(monitoring_latency=0.5)
                return c.temperature
            except Exception as e:
                log.error(e)

        return NOTIMPLEMENTED_NUMERICAL

def measure_core(metric, args):
    
    if metric == "info":
        if cpuinfo:
            return cpuinfo.brand
    elif metric == "frequency":
        if cpuinfo:
            return cpuinfo.get_cpu_info()["hz_actual_raw"][0]
    elif metric == "usage":
        if psutil:
            psutil.cpu_percent(percpu=True)[args]
    elif metric == "temperature":
        return NOTIMPLEMENTED_NUMERICAL
def measure_gpu(metric, args):
    if metric == "info":
        return NOTIMPLEMENTED_TEXT
    elif metric == "gpuclock":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "memclock":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "vramusage":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "temperature":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "usage":
        return NOTIMPLEMENTED_NUMERICAL

def measure_memory(metric, args):
    if metric == "total":
        return psutil.virtual_memory().total
    elif metric == "free":
        return psutil.virtual_memory().available
    elif metric == "used":
        return psutil.virtual_memory().used

def measure_process(metric, args):
    if metric == "cpuusage":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "memusage":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "name":
        return NOTIMPLEMENTED_TEXT

def measure_partition(metric, args):
    if metric == "totalspace":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "freespace":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "usedspace":
        return NOTIMPLEMENTED_NUMERICAL
    
def measure_disk(metric, args):
    if metric == "temperature":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "status":
        return NOTIMPLEMENTED_NUMERICAL


def measure_network(metric, args):
    if metric == "info":
        return NOTIMPLEMENTED_TEXT
    elif metric == "receivepersec":
        return NOTIMPLEMENTED_NUMERICAL
    elif metric == "transmitpersec":
        return NOTIMPLEMENTED_NUMERICAL

def get_system_data(metric):
    if metric == "cpus":
        return list(range(1))
    if metric == "cores":
        return get_core_list()
    if metric == "gpus":
        return list(range(1))
    if metric == "disks":
        return list(range(0))
    if metric == "partitions":
        return get_partition_list()
    if metric == "processes":
        return get_process_list()
    if metric == "networks":
        return getNetworkInterfaces()


def getNetworkInterfaces():
    ''' Gets the names of all currently available network interfaces and returns them in an array '''
    if not psutil:
        return []
    try:
        detailed_interfaces = psutil.net_if_stats()
    except Exception as e:
        log.error(e)
        log.error("Couldn't get network interfaces")
        detailed_interfaces = {}
    simple_interfaces = []
    for interface in detailed_interfaces:
        simple_interfaces.append(interface)
    return simple_interfaces


def get_core_list():
    result = []
    try:
        list(range(psutil.cpu_count()))
    except Exception as e:
        log.error("Couldn't get corelist")
        log.error(e)
    return result


def get_partition_list():
    result = []
    try:
        result = psutil.disk_partitions()
    except Exception as e:
        log.error("Couldn't get partition list")
        log.error(e)
    return result


def get_process_list():
    result = []
    try:
        result = psutil.pids()
    except Exception as e:
        log.error("Couldn't get processlist")
        log.error(e)
    return result


def get_operating_system():
    log.info("Retrieving operating system")
    baseName = sys.platform
    if baseName.startswith("linux"):
        return Operating_System.linux
    elif baseName.startswith("win"):
        return Operating_System.windows
    elif baseName.startswith("darwin"):
        return Operating_System.macos
    elif baseName.startswith("freebsd"):
        return Operating_System.freebsd
    return None 


currentOS = get_operating_system()
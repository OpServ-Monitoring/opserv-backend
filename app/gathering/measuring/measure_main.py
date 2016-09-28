#
# Main file for the different hardware and valueType measure methods
#
# 27.09.2016
#
#


from app.misc.helper import importIfExists

# Optional depency importing
psutil = importIfExists("psutil")
pynvml = importIfExists("pynvml")
pyspectator = importIfExists("pyspectator")

NOTIMPLEMENTED_NUMERICAL = 0
NOTIMPLEMENTED_TEXT = ""


def measure_cpu(valueType, args):
    if valueType == "usage":
        return psutil.cpu_percent()
    elif valueType == "frequency":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "info":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "temperature":
        return NOTIMPLEMENTED_NUMERICAL

def measure_core(valueType, args):
    
    if valueType == "info":
        return NOTIMPLEMENTED_TEXT
    elif valueType == "frequency":
        return NOTIMPLEMENTED_NUMERICAL
    elif valueType == "usage":
        return NOTIMPLEMENTED_NUMERICAL
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
        return str([])
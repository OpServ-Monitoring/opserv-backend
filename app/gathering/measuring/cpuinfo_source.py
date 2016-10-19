'''
    This module contains the cpuinfo wrapper class that exposes the cpuinfo module

    The original sources for this data is as folloiwng:

    Windows Registry (Windows)
    /proc/cpuinfo (Linux)
    sysctl (OS X)
    dmesg (Unix/Linux)
    isainfo and kstat (Solaris)
    cpufreq-info (BeagleBone)
    lscpu (Unix/Linux)
    sysinfo (Haiku)
    Querying the CPUID register (Intel X86 CPUs)
    From https://github.com/workhorsy/py-cpuinfo
'''

from misc.constants import Operating_System
from misc.helper import importIfExists
from gathering.measuring.MeasuringSource import MeasuringSource

class PyCpuInfoSource(MeasuringSource):
    '''
        Source description
    '''

    _supported_os = [Operating_System.windows, Operating_System.macos,
                     Operating_System.linux, Operating_System.freebsd]
    _supported_comps = {
        "cpu" : {
            "info",
            "frequency"
        },
        "core" : {
            "info",
            "frequency"
        },
        "system": {
            "cores"
        }
    }

    def __init__(self):
        self._init_complete = False
        self.cpuinfo = importIfExists("cpuinfo")

        if self.cpuinfo:
            self._init_complete = True

    def init(self):
        '''
            Initializes the measuring source (opening hardware connections etc.)
            If initialization is successful, it will return True
            If errors occured, the return value will be False
        '''
        pass

    def deinit(self):
        '''
            De-Initializes the measuring source, removing connections etc.
            Returns True if deinit was successfull, False if it errord
        '''
        pass

    def get_measurement(self, component, metric, args):
        '''
            Retrieves a measurement from the measuring source
            given the component, metric and optionally arguments
        '''
        if component == "cpu":
            if metric == "info":
                return self.cpuinfo.get_cpu_info()["brand"]
            elif metric == "frequency":
                return self.cpuinfo.get_cpu_info()["hz_actual_raw"][0]
        elif component == "core":
            if metric == "info":
                return self.cpuinfo.get_cpu_info()["brand"] + "Core #" + str(args)
            elif metric == "frequency":
                return self.cpuinfo.get_cpu_info()["hz_actual_raw"][0]
        elif component == "system":
            if metric == "cores":
                return self.cpuinfo.get_cpu_info()["count"]

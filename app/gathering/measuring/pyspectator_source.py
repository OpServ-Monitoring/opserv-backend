'''
    Wrapper class for the pyspactor module to be used in the system
    PySpectator gets most of it's valuable data from wmi and pythoncom modules.
    These are pretty likely to fail especially on laptops
    The rest is a mix of psutil usage and simple Linux file access
    Also it uses the netifaces module for network data, the module is nice
    enough to give it its own wrapper here
'''

from misc.constants import Operating_System
from misc.helper import importIfExists
from gathering.measuring.MeasuringSource import MeasuringSource

class PySpectatorSource(MeasuringSource):
    '''
        Source description
    '''

    _supported_os = [Operating_System.windows, Operating_System.linux]
    _supported_comps = {
        "cpu" : {
            "temperature"
        }
    }

    def __init__(self):

        self._init_complete = False

        self.pyspectator = importIfExists("pyspectator.processor")

        if self.pyspectator:
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
            if metric == "temperature":
                cpu = self.pyspectator.CPU(monitoring_latency=1)
                with cpu:
                    return cpu.temperature

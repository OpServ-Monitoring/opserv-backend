'''
    This module is a null-interface for measuring values
    It only implements returning default numbers and is used for debugging purposes
'''

from gathering.measuring.MeasuringSource import MeasuringSource

from misc.constants import implemented_hardware, Operating_System

NOTIMPLEMENTED_NUMERICAL = 0
NOTIMPLEMENTED_TEXT = ""


class NullSource(MeasuringSource):
    '''
        Null Source, returns default values for all the existing components
    '''
    _supported_comps = implemented_hardware
    _supported_os = [Operating_System.macos, Operating_System.windows, Operating_System.linux]

    def __init__(self):
        pass

    def init(self):
        '''
            Initializes the measuring source (opening hardware connections etc.)
            If initialization is successful, it will return True
            If errors occured, the return value will be False
        '''
        return True

    def deinit(self):
        '''
            De-Initializes the measuring source, removing connections etc.
            Returns True if deinit was successfull, False if it errord
        '''
        return True

    def get_measurement(self, component, metric, args):
        '''
            Retrieves a measurement from the measuring source
            given the component, metric and optionally arguments
        '''
        if component == "system":
            if metric == "cpus":
                return [0]
            return []
        return NOTIMPLEMENTED_NUMERICAL

'''
    This module is a generic not implemented source
'''

from gathering.measuring.MeasuringSource import MeasuringSource
from misc.constants import Operating_System

class GenericSource(MeasuringSource):
    '''
        Source description
    '''

    _supported_os = [Operating_System.linux]
    _supported_comps = {

    }

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
        pass

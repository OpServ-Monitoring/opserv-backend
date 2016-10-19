'''
    This module contains the abstract base class for the measuring sources
'''

from abc import ABCMeta, abstractmethod, abstractproperty

class MeasuringSource(metaclass=ABCMeta):
    '''
        Abstract interface, which the measuring source implements
    '''
    @abstractproperty
    def _supported_os(self):
        ''' Array of Operating_System enums, that contain the supported operating systems '''
        pass
    @abstractproperty
    def _supported_comps(self):
        '''
            Dictionary of supported components, which are itself dictionaries of supported metrics
        '''
        pass


    @abstractmethod
    def init(self):
        '''
            Initializes the measuring source (opening hardware connections etc.)
            If initialization is successful, it will return True
            If errors occured, the return value will be False
        '''
        pass

    @abstractmethod
    def deinit(self):
        '''
            De-Initializes the measuring source, removing connections etc.
            Returns True if deinit was successfull, False if it errord
        '''
        pass

    @abstractmethod
    def get_measurement(self, component, metric, args):
        '''
            Retrieves a measurement from the measuring source
            given the component, metric and optionally arguments
        '''
        pass


    def can_measure(self, component, metric):
        '''
            Checks whether the source can measure the specified component metric combo
        '''
        if component in self._supported_comps:
            if metric in self._supported_comps[component]:
                return True
        return False


    def get_supported_comps(self):
        '''
            Returns a list of all the components and their metrics
            that the measuring source supports
        '''
        return self._supported_comps


    def get_supported_os(self):
        '''
            Returns a list of supported operating systems
        '''
        return self._supported_os


    def os_is_supported(self, current_os):
        '''
            Returns True if the given operating system is supported
            and False if it not
        '''
        if current_os in self._supported_os:
            return True
        return False

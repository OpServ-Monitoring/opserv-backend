'''
    This module is a implemented source that retuns the
    cpu temperature and the core frequency from a Rassberry Pi
    Author: Georg Rose, 2016
'''

from misc.constants import Operating_System
from gathering.measuring.MeasuringSource import MeasuringSource

RASPI_TEMP_FILE = '/sys/class/thermal/thermal_zone0/temp'
RASPI_FREQ_PATH = '/sys/devices/system/cpu/cpu{}/cpufreq/scaling_cur_freq'


class RaspiTempSource(MeasuringSource):
    '''
        Source description
    '''

    _supported_os = [Operating_System.linux]
    _supported_comps = {
        "cpu" : {
            "temperature"
        },
        "core" : {
            "frequency"
            }
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
            Reads the temperature and frequency out of a file.
            Temprature needs to be converted from millicentigrade to centigrade.
        '''
        if component == "cpu":
            if metric == "temperature":
                file_handle = open(RASPI_TEMP_FILE, 'r')
                temp = file_handle.read()
                file_handle.close()
                temp = float(temp)/1000.0
                return temp
        if component == "core":
            if metric == "frequency":
                file_handle = open(RASPI_FREQ_PATH.format(args), 'r')
                frequency = file_handle.read()
                file_handle.close()
                return frequency

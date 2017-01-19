'''
    Contains class for the Gatherer
'''
import logging
import time
from collections import namedtuple

from gathering.measurement_manager import MeasurementManager

log = logging.getLogger("opserv." + __name__)
GatherPerformanceTuple = namedtuple("GatherPerformanceTuple", ["key", "time"])

class Gatherer():
    '''
        Contains information about a gathering rate
        Each gathering rate gets its own gatherer to keep track of its properties and
        lifecycle.
    '''
    def __init__(self, component, metric, args, delayms, event=None):
        log.debug("New Gatherer created with: %s,%s,%s,%d", component, metric, args, delayms)
        self.component = component
        self.metric = metric
        self.args = args
        self.delayms = delayms
        self.event = event
        self.last_measure_time = 0


    def set_rate(self, delayms):
        '''
            Setter for the gathering rate of the gatherer e.g.
            how often the gatherer will measure
            Note, that this does not reset the current event in the scheduler
        '''
        self.delayms = delayms


    def measure(self):
        '''
            Measures the in the instance specified comp/metric/args by calling
            the measurement manager with the instance's properties
        '''
        before_measure_time = time.time()
        MeasurementManager.make_measurement(self.component, self.metric, self.args)
        self.last_measure_time = time.time() - before_measure_time

    def set_event(self, event):
        '''
            Setter for the event property. note that this does not reflect an
            update in the scheduler. The event has to be cancelled there too.
        '''
        self.event = event


    def get_key(self):
        '''
            Generates a dictionary key for use in the gatherer_manager to find each Gatherer
            instantly
        '''
        return (self.component, self.metric, self.args)

    def get_performance_tuple(self):
        '''
            Creates a tuple specified by GatherPerformanceTuple
            and returns it
        '''
        return GatherPerformanceTuple(self.get_key(), self.last_measure_time)

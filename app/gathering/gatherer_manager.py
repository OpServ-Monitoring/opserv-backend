"""
    Main module for gathering manager class
"""
import logging
import sched
import time

from gathering.gatherer import Gatherer
from gathering.measurement_manager import MeasurementManager
from misc.constants import MINIMUM_GATHERING_RATE

GATHERING_EVENT_PRIORITY = 1

log = logging.getLogger("opserv." + __name__)


class GathererManager():
    '''
        Manages the gathering of rates and data requests
        I.e. keeps track of all the enabled gatherers and how they are performing
        Also formally handles the queuelisteners events
    '''
    scheduler = sched.scheduler(time.time, time.sleep)
    gatherers = {}

    @classmethod
    def init_manager(cls):
        '''
            Initializes the manager and all the required other classes
        '''
        MeasurementManager.init_manager()

    @classmethod
    def handle_new_rate(cls, new_rate):
        '''
            Parses, validates and processes new data gathering rates coming from the REST-API
            or out of the database
            This basically creates a new gatherer or updates/deletes existing ones based
            on the given delayms
        '''
        if not rate_update_valid(new_rate):
            log.error("Received invalid gathering rate: %s", str(new_rate))
            return

        log.debug("Received new gathering rate: %s", str(new_rate))
        comp = new_rate["component"]
        metric = new_rate["metric"]
        args = new_rate["args"]
        delayms = int(new_rate["delayms"])

        if delayms == 0:
            cls.remove_gatherer(comp, metric, args)
            return

        elif delayms < MINIMUM_GATHERING_RATE:
            log.error("Tried to create gatherer with delayms < minimum constant")
            log.info("Gathering rate will be clamped to minimum delayms")
            delayms = max(MINIMUM_GATHERING_RATE, delayms)

        if cls.gatherer_exists(comp, metric, args):
            cls.update_gatherer(comp, metric, args, delayms)
        else:
            cls.create_new_gatherer(comp, metric, args, delayms)

    @classmethod
    def handle_data_request(cls, new_request):
        '''
            Handles data requests coming from the REST-API
            This is basically a one shot update on a specific comp/metric/args combo
            Which takes a new measurement once
        '''
        if not request_valid(new_request):
            log.error("Received invalid data request: %s", str(new_request))
            return

        comp = new_request["component"]
        metric = new_request["metric"]
        args = new_request["args"]

        MeasurementManager.make_measurement(comp, metric, args)

    @classmethod
    def create_new_gatherer(cls, component, metric, args, delayms):
        '''
            Creates a new gatherer instance with corresponding event in the scheduler
            and inserts it into the gatherers list.
            Also immediately requests a data update to take a measurement instantly.
        '''
        log.debug("Creating new Gatherer with the following specifications: %s, %s, %s, %d",
                  component, metric, str(args), delayms)

        new_gatherer = Gatherer(component, metric, args, delayms)
        cls.gatherers[new_gatherer.get_key()] = new_gatherer

        cls.handle_gathering_event(gather_obj=new_gatherer)

    @classmethod
    def handle_gathering_event(cls, gather_obj):
        '''
            This is the method called by the scheduler when an event expires
            This basically takes the gatherer instance given as args to the scheduler
            And calls its measurement function.
            To avoid timing issues while measuring a new event for the next call is
            created before the measurement call.
        '''
        delay_in_sec = ms_to_sec(gather_obj.delayms)
        new_gather_event = cls.scheduler.enter(delay_in_sec, GATHERING_EVENT_PRIORITY,
                                               cls.handle_gathering_event,
                                               kwargs={
                                                   "gather_obj": gather_obj
                                               })

        gather_obj.set_event(new_gather_event)

        gather_obj.measure()

    @classmethod
    def check_for_expired_events(cls):
        '''
            This method contains the event expiration checking from the scheduler
            It has to be called pretty often to avoid timing issues and should
            not contain huge logic/performance hungry code.
        '''
        cls.scheduler.run(blocking=False)

    @classmethod
    def update_gatherer(cls, comp, metric, args, delayms):
        '''
            This method updates the in the arguments specified gatherer, assuming
            it already exists, with the given delayms number
            Then it calls a data update to get fresh data instantly
        '''
        log.debug("Updating existing Gatherer with the following specifications: %s, %s, %s, %d",
                  comp, metric, args, delayms)
        changed_gatherer = cls.get_gatherer(comp, metric, args)
        changed_gatherer.set_rate(delayms)
        cls.scheduler.cancel(changed_gatherer.event)
        cls.handle_gathering_event(changed_gatherer)

    @classmethod
    def gatherer_exists(cls, comp, metric, args):
        '''
            Checks whether the in the arguments given gatherer already exists and
            returns a boolean with the result
        '''
        return (comp, metric, args) in cls.gatherers

    @classmethod
    def get_gatherer(cls, comp, metric, args):
        '''
            Returns the gatherer instance specified in the argumenst if it does not
            exists the return value is None
        '''
        if cls.gatherer_exists(comp, metric, args):
            return cls.gatherers[(comp, metric, args)]
        else:
            return None

    @classmethod
    def remove_gatherer(cls, component, metric, args):
        '''
            Removes the in the arguments specified gatherer, assuming it already exists
        '''
        if cls.gatherer_exists(component, metric, args):
            cls.scheduler.cancel(cls.gatherers[(component, metric, args)].event)
            del cls.gatherers[(component, metric, args)]
        else:
            log.error("Trying to delete gatherer that doesn't exist: %s, %s, %s",
                      component, metric, args)

    @classmethod
    def get_gatherer_count(cls):
        '''
            Returns the current number of the gatherers that are active
        '''
        return len(cls.gatherers)

    @classmethod
    def get_measuring_times(cls):
        '''
            Returns the GatherPerformanceTuple containing performance information about
            gatherers for each active gatherer
        '''
        gather_times = []
        for gather_key in cls.gatherers:
            current_gath = cls.gatherers[gather_key]
            gather_times.append(current_gath.get_performance_tuple())

        return gather_times


def ms_to_sec(milliseconds):
    '''
        Converts milliseconds to sec
        Used often to convert between Javascript Unix time and Python Unix time
    '''
    return milliseconds / 1000


def request_valid(request):
    """
        Checks the given request for the correct data structure
        Returns True if it has the right structure
    """
    if request is not None:
        if "component" in request and "metric" in request:
            if "args" in request:
                return True
            else:
                request["args"] = None
                return True
    return False


def rate_update_valid(rate_update):
    """
        Checks the given rate_update for the correct data structure
        Returns True if it has the right structure
    """
    if rate_update is not None:
        if "component" in rate_update and "metric" in rate_update and "delayms" in rate_update:
            if "args" in rate_update:
                return True
            else:
                rate_update["args"] = None
                return True
            return True
    return False

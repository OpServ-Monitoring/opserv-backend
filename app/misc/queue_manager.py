"""
    This module contains the queue manager which initalizes, handles and exposes 
    most of the communication functionality between server and gathering thread
"""

from queue import Queue

from misc.constants import QUEUEMANAGER_DEFAULT_TIMEOUT
from misc.opserv_helper import check_comp_args

request_data_queue = None
set_gathering_rate_queue = None

realtime_queues = None


def init():
    """
        Initializes the queue manager
    """
    global request_data_queue
    global set_gathering_rate_queue
    global realtime_queues

    request_data_queue = Queue()
    set_gathering_rate_queue = Queue()

    realtime_queues = {
        "cpu": {},
        "cpucore": {},
        "gpu": {},
        "memory": {},
        "disk": {},
        "partition": {},
        "process": {},
        "network": {},
        "system": {}
    }


def get_queue(component, metric, args=None):
    """ Returns either the requested queue or creates a new one """
    args = check_comp_args(realtime_queues, component, args)

    create_queue_if_not_exists(component, metric, args)

    if args is not None:
        return realtime_queues[component][args][metric]
    else:
        return realtime_queues[component][metric]


def remove_queue(component, metric, args=None):
    """Removes the specified queue from the dict"""
    args = check_comp_args(realtime_queues, component, args)

    if queue_exists(component, metric, args):
        if args:
            realtime_queues[component][args][metric] = None
        else:
            realtime_queues[component][metric] = None


def create_queue_if_not_exists(component, metric, args):
    """ Creates a new Queue if the specified one doesn't already exists """
    if not queue_exists(component, metric, args):
        if args is not None:
            realtime_queues[component][args][metric] = Queue()
        else:
            realtime_queues[component][metric] = Queue()


def queue_exists(component, metric, args):
    """ Checks whether the specified queue already exists """
    if component in realtime_queues:
        if args is not None:
            if args in realtime_queues[component] and metric in realtime_queues[component][args]:
                return True
        elif metric in realtime_queues[component]:
            return True

    return False


def put_measurement_into_queue(component, metric, measurement, args=None):
    """ Puts the given measurement into the specified queue """
    args = check_comp_args(realtime_queues, component, args)

    get_queue(component, metric, args).put(measurement)


def read_measurement_from_queue(component, metric, args=None, blocking=False,
                                timeout=QUEUEMANAGER_DEFAULT_TIMEOUT):
    """ Get a single measurement from the specified queue.
        Warning, could cause Timeout Errors"""
    args = check_comp_args(realtime_queues, component, args)

    if (not get_queue(component, metric, args).empty()) or blocking == True:
        return get_queue(component, metric, args).get(blocking, timeout)
    else:
        return None


def real_time_queue_empty(component, metric, args=None):
    return get_queue(component, metric, args).empty()


def set_gathering_rate(component, metric, delayms, args=None):
    """ Send a gathering rate update that will update the queue and realtime data directory
        in the interval specified with delayms """
    args = check_comp_args(realtime_queues, component, args)

    set_gathering_rate_queue.put({
        "component": component,
        "metric": metric,
        "args": args,
        "delayms": delayms
    })


def request_data(component, metric, args=None):
    """ Request a single data update that gets send into the queue and realtime data dictionary """
    args = check_comp_args(realtime_queues, component, args)

    request_data_queue.put({
        "component": component,
        "metric": metric,
        "args": args
    })

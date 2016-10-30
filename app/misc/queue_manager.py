"""
    This module contains the queue manager which initalizes, handles and exposes 
    most of the communication functionality between server and gathering thread
"""

from queue import Queue

from misc.constants import QUEUEMANAGER_DEFAULT_TIMEOUT
from misc.helper import check_comp_args

requestDataQueue = None
setGatheringRateQueue = None

realtimeQueues = None


def init():
    """
        Initializes the queue manager
    """
    global requestDataQueue
    global setGatheringRateQueue
    global realtimeQueues

    requestDataQueue = Queue()
    setGatheringRateQueue = Queue()

    realtimeQueues = {
        "cpu": {},
        "core": {},
        "gpu": {},
        "memory": {},
        "disk": {},
        "partition": {},
        "process": {},
        "network": {},
        "system": {}
    }


def getQueue(component, metric, args=None):
    """ Returns either the requested queue or creates a new one """
    check_comp_args(realtimeQueues, component, args)

    createQueueIfNotExists(component, metric, args)

    if args != None:
        return realtimeQueues[component][args][metric]
    else:
        return realtimeQueues[component][metric]


def removeQueue(component, metric, args):
    """Removes the specified queue from the dict"""
    if queueExists(component, metric, args):
        if args:
            realtimeQueues[component][args][metric] = None
        else:
            realtimeQueues[component][metric] = None


def createQueueIfNotExists(component, metric, args):
    """ Creates a new Queue if the specified one doesn't already exists """
    if not queueExists(component, metric, args):
        if args != None:
            realtimeQueues[component][args][metric] = Queue()
        else:
            realtimeQueues[component][metric] = Queue()


def queueExists(component, metric, args):
    """ Checks whether the specified queue already exists """
    if component in realtimeQueues:
        if args != None:
            if args in realtimeQueues[component]:
                if metric in realtimeQueues[component][args]:
                    return True
        else:
            if metric in realtimeQueues[component]:
                return True
    return False


def putMeasurementIntoQueue(component, metric, measurement, args=None):
    """ Puts the given measurement into the specified queue """
    getQueue(component, metric, args).put(measurement)


def readMeasurementFromQueue(component, metric, args=None, blocking=False,
                             timeout=QUEUEMANAGER_DEFAULT_TIMEOUT):
    """ Get a single measurement from the specified queue.
        Warning, could cause Timeout Errors"""
    if (not getQueue(component, metric, args).empty()) or blocking == True:
        return getQueue(component, metric, args).get(blocking, timeout)
    else:
        return None


def real_time_queue_empty(component, metric, args=None):
    if getQueue(component, metric, args).empty():
        return True
    else:
        return False


def setGatheringRate(component, metric, delayms, args=None):
    """ Send a gathering rate update that will update the queue and realtime data directory
        in the interval specified with delayms """
    setGatheringRateQueue.put({
        "component": component,
        "metric": metric,
        "args": args,
        "delayms": delayms
    })


def requestData(component, metric, args=None):
    """ Request a single data update that gets send into the queue and realtime data dictionary """
    requestDataQueue.put({
        "component": component,
        "metric": metric,
        "args": args
    })

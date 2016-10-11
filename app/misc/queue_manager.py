from queue import Queue

from misc.constants import HARDWARE_DEFAULTS
from misc.helper import argumentHasDefault, argumentIsOptional, createSubDictIfNecessary, assertComponentExists

requestDataQueue = None
setGatheringRateQueue = None

realtimeQueues = None

def init():
    global requestDataQueue
    global setGatheringRateQueue
    global realtimeQueues
    
    requestDataQueue = Queue()
    setGatheringRateQueue = Queue()

    realtimeQueues = {
        "cpu": {},
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
    # Check if the component exists
    assertComponentExists(realtimeQueues, component)
    # TODO MORE ASSERTS ON ARGS & metric

    # If no argument is given
    if not args:
        if argumentIsOptional(component):
            args = None
        elif argumentHasDefault(component):
            args = HARDWARE_DEFAULTS[component][1]
        else:
            raise Exception("Trying to access queue without specifying the argument. component: {}".format(component))

    createSubDictIfNecessary(realtimeQueues, component, args)
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
    """ Checks whehter the specified queue already exists """
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


def readMeasurementFromQueue(component, metric, args=None, blocking=False, timeout=None):
    """ Get a single measurement from the specified queue.
        Warning, could cause QueueEmpty Errors"""
    return getQueue(component, metric, args).get(blocking, timeout)


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

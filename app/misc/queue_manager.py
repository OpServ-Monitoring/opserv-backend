from queue import Queue

from misc.constants import HARDWARE_DEFAULTS
from misc.helper import argumentHasDefault, argumentIsOptional, createSubDictIfNecessary, assertHardwareExists

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


def getQueue(hardware, valueType, args=None):
    """ Returns either the requested queue or creates a new one """
    # Check if the hardware exists
    assertHardwareExists(realtimeQueues, hardware)
    # TODO MORE ASSERTS ON ARGS & VALUETYPE

    # If no argument is given
    if not args:
        if argumentIsOptional(hardware):
            args = None
        elif argumentHasDefault(hardware):
            args = HARDWARE_DEFAULTS[hardware][1]
        else:
            raise Exception("Trying to access queue without specifying the argument. Hardware: {}".format(hardware))

    createSubDictIfNecessary(realtimeQueues, hardware, args)
    createQueueIfNotExists(hardware, valueType, args)

    if args != None:
        return realtimeQueues[hardware][args][valueType]
    else:
        return realtimeQueues[hardware][valueType]


def removeQueue(hardware, valueType, args):
    """Removes the specified queue from the dict"""
    if queueExists(hardware, valueType, args):
        if args:
            realtimeQueues[hardware][args][valueType] = None
        else:
            realtimeQueues[hardware][valueType] = None


def createQueueIfNotExists(hardware, valueType, args):
    """ Creates a new Queue if the specified one doesn't already exists """
    if not queueExists(hardware, valueType, args):
        if args != None:
            realtimeQueues[hardware][args][valueType] = Queue()
        else:
            realtimeQueues[hardware][valueType] = Queue()


def queueExists(hardware, valueType, args):
    """ Checks whehter the specified queue already exists """
    if hardware in realtimeQueues:
        if args != None:
            if args in realtimeQueues[hardware]:
                if valueType in realtimeQueues[hardware][args]:
                    return True
        else:
            if valueType in realtimeQueues[hardware]:
                return True
    return False


def putMeasurementIntoQueue(component, metric, measurement, args=None):
    """ Puts the given measurement into the specified queue """
    getQueue(component, metric, args).put(measurement)


def readMeasurementFromQueue(component, metric, args=None):
    """ Get a single measurement from the specified queue.
        Warning, could cause QueueEmpty Errors"""
    return getQueue(component, metric, args).get()


def setGatheringRate(component, metric, delayms, args=None):
    """ Send a gathering rate update that will update the queue and realtime data directory
        in the interval specified with delayms """
    setGatheringRateQueue.put({
        "hardware": component,
        "valueType": metric,
        "args": args,
        "delayms": delayms
    })


def requestData(component, metric, args=None):
    """ Request a single data update that gets send into the queue and realtime data dictionary """
    requestDataQueue.put({
        "hardware": component,
        "valueType": metric,
        "args": args
    })

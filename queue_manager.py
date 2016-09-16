#
# Queue File for using the same queues within the project
#
# 27.08.2016
#
# Example usage:
#
# import queues
# queues.requestDataQueue.put("givememoredata")
# print(queues.requestDataQueue.get())
#

from queue import Queue

requestDataQueue = Queue()
setGatheringRateQueue = Queue()

realtimeQueues = {
    "cpu" : {},
    "gpu" : {},
    "memory" : {},
    "disk" : {},
    "fs" : {},
    "process" : {},
    "system" : {}
}

# This described the default values aswell as whether specific hardware requires additional argument information
# The tuple has this structure: (ARGUMENTNECESSARY, DEFAULTVALUE)
REALTIME_DEFAULTS = {
    "cpu" : (True, 0),
    "gpu" : (True, 0),
    "memory" : (False, None),
    "disk" : (True, None),
    "fs" : (True, None),
    "process" :  (True, "all"),
    "system" : (False, None)
}


""" Returns either the requested queue or creates a new one """
def getQueue(hardware, valueType, args=None):
    # Check if the hardware exists
    assertHardwareExists(hardware)
    # TODO MORE ASSERTS ON ARGS & VALUETYPE
    
    # If no argument is given
    if not args:
        if argumentIsOptional(hardware):
            args = None
        elif argumentHasDefault(hardware):
            args = REALTIME_DEFAULTS[hardware][1]
        else:
            raise Exception("Trying to access queue without specifying the argument. Hardware: {}".format(hardware))

    createSubDictIfNecessary(hardware, args)
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


def argumentIsOptional(hardware):
    """ Checks whether for the given hardware an argument is optional """
    return not REALTIME_DEFAULTS[hardware][0]



def argumentHasDefault(hardware):
    """ Checks whether the given hardware has a default argument """
    if REALTIME_DEFAULTS[hardware][1] != None:
        return True
    return False



def createSubDictIfNecessary(hardware, args):
    """ Creates a sub-dictionary for arguments if there isn't already one existing and the arguments is not None"""
    if args == None:
        return
    if not args in realtimeQueues[hardware]:
        realtimeQueues[hardware][args] = {}



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



def assertHardwareExists(hardware):
    """ Simple assert to check if the given hardware exists in the constants and realtime dict """
    if not hardware in realtimeQueues or not hardware in REALTIME_DEFAULTS:
        raise NotImplementedError(hardware)
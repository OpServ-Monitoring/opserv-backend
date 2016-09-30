#
# Data manager used for transfering data between the gathering and server thread
#
# The Real-Time is deprecated right now
#
#
# 27.08.2016
#
# Example usage:
#
# import data_manager
# data_manager.getMeasurement("cpu", "usage")
#
 
from misc.constants import HARDWARE_DEFAULTS
 
from misc.helper import argumentHasDefault, argumentIsOptional, createSubDictIfNecessary, assertHardwareExists

realtimeData = {
    "cpu": {},
    "gpu": {},
    "memory": {},
    "disk": {},
    "partition": {},
    "process": {},
    "network": {},
    "system": {}
}    


def getMeasurement(component, metric, args=None):
    """ Returns the currently saved realtime data of the specified component """
    # Check if the hardware exists
    assertHardwareExists(realtimeData, component)
    # TODO MORE ASSERTS ON ARGS & VALUETYPE

    # If no argument is given
    if not args:
        if argumentIsOptional(component):
            args = None
        elif argumentHasDefault(component):
            args = HARDWARE_DEFAULTS[component][1]
        else:
            raise Exception("Trying to access data without specifying the argument. Hardware: {}".format(component))

    createSubDictIfNecessary(realtimeData, component, args)
    createMeasurementIfNotExists(component, metric, args)

    if args != None:
        return realtimeData[component][args][metric]
    else:
        return realtimeData[component][metric]

def setMeasurement(component, metric, value, args=None):
    """ Sets the specified metric to the desired value"""
    # Check if the hardware exists
    assertHardwareExists(realtimeData, component)
    # TODO MORE ASSERTS ON ARGS & VALUETYPE

    # If no argument is given
    if not args:
        if argumentIsOptional(component):
            args = None
        elif argumentHasDefault(component):
            args = HARDWARE_DEFAULTS[component][1]
        else:
            raise Exception("Trying to access data without specifying the argument. Hardware: {}".format(component))

    createSubDictIfNecessary(realtimeData, component, args)
    createMeasurementIfNotExists(component, metric, args)

    if args != None:
        realtimeData[component][args][metric] = value
    else:
        realtimeData[component][metric] = value

def createMeasurementIfNotExists(hardware, valueType, args):
    """ Creates a new variable if the specified one doesn't already exists """
    if args == None:
        if not valueType in realtimeData[hardware]:
            realtimeData[hardware][valueType] = None
    else:
        if not valueType in realtimeData[hardware][args]:
            realtimeData[hardware][args][valueType] = None
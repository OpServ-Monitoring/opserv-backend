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
 
from misc.helper import check_comp_args

realtimeData = None


def init():
    """
        Initializes the data manager
    """
    global realtimeData

    realtimeData = {
        "cpu": {},
        "core" : {},
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
    check_comp_args(realtimeData, component, args)

    createMeasurementIfNotExists(component, metric, args)

    if args != None:
        return realtimeData[component][args][metric]
    else:
        return realtimeData[component][metric]

def setMeasurement(component, metric, value, args=None):
    """ Sets the specified metric to the desired value"""
    check_comp_args(realtimeData, component, args)

    createMeasurementIfNotExists(component, metric, args)

    if args != None:
        realtimeData[component][args][metric] = value
    else:
        realtimeData[component][metric] = value

def createMeasurementIfNotExists(component, metric, args):
    """ Creates a new variable if the specified one doesn't already exists """
    if args == None:
        if not metric in realtimeData[component]:
            realtimeData[component][metric] = None
    else:
        if not metric in realtimeData[component][args]:
            realtimeData[component][args][metric] = None

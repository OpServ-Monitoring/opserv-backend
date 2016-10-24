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
 
from misc.helper import argument_has_default, argument_is_optional,\
                        create_subdict_if_necessary, assert_component_exists,\
                        assert_argument_value

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
    assert_component_exists(realtimeData, component)
    # If no argument is given
    assert_argument_value(component, args)

    create_subdict_if_necessary(realtimeData, component, args)
    createMeasurementIfNotExists(component, metric, args)

    if args != None:
        return realtimeData[component][args][metric]
    else:
        return realtimeData[component][metric]

def setMeasurement(component, metric, value, args=None):
    """ Sets the specified metric to the desired value"""
    # Check if the component exists
    assert_component_exists(realtimeData, component)
    # TODO MORE ASSERTS ON ARGS & metric

    assert_argument_value(component, args)

    create_subdict_if_necessary(realtimeData, component, args)
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

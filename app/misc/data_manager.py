'''#
Data manager used for transfering data between the gathering and server thread

27.08.2016

Example usage:

import data_manager
data_manager.get_measurement("cpu", "usage")
'''
from misc.helper import check_comp_args

realtime_data = None


def init():
    """
        Initializes the data manager
    """
    global realtime_data

    realtime_data = {
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


def get_measurement(component, metric, args=None):
    """ Returns the currently saved realtime data of the specified component """
    args = check_comp_args(realtime_data, component, args)

    create_measurement_if_not_exists(component, metric, args)

    if args is not None:
        return realtime_data[component][args][metric]
    else:
        return realtime_data[component][metric]


def set_measurement(component, metric, value, args=None):
    """ Sets the specified metric to the desired value"""
    args = check_comp_args(realtime_data, component, args)

    create_measurement_if_not_exists(component, metric, args)

    if args is not None:
        realtime_data[component][args][metric] = value
    else:
        realtime_data[component][metric] = value


def create_measurement_if_not_exists(component, metric, args):
    """ Creates a new variable if the specified one doesn't already exists """
    if args is None:
        if not metric in realtime_data[component]:
            realtime_data[component][metric] = None
    else:
        if not args in realtime_data[component]:
            print("wtf")
        if not metric in realtime_data[component][args]:
            realtime_data[component][args][metric] = None

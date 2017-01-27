

"""
    Helper Module to help you through the ups and down of the project
"""


from misc.constants import HARDWARE_DEFAULTS, Operating_System
import sys

def argument_is_optional(hardware):
    """ Checks whether for the given hardware an argument is optional """
    return not HARDWARE_DEFAULTS[hardware][0]


def argument_has_default(hardware):
    """ Checks whether the given hardware has a default argument """
    if HARDWARE_DEFAULTS[hardware][1] is not None:
        return True
    return False


def create_subdict_if_necessary(main_dict, hardware, args):
    """
        Creates a sub-dictionary for arguments if there isn't
        already one existing and the arguments is not None
    """
    assert_is_dict(main_dict)

    if args is None:
        return
    if not args in main_dict[hardware]:
        main_dict[hardware][args] = {}


def assert_component_exists(main_dict, hardware):
    """ Simple assert to check if the given hardware exists in the constants and realtime dict """
    if not hardware in main_dict or not hardware in HARDWARE_DEFAULTS:
        raise NotImplementedError(hardware)


def assert_is_dict(dict_to_test):
    """
        Returns true if the argument is a dictionary and
        raises typeerror if it is not
    """
    if isinstance(dict_to_test, dict):
        return True
    else:
        raise TypeError("This should be a dict" + str(dict_to_test))


def get_operating_system():
    """
        Returns the current operating system as an enumeration item
    """
    base_name = sys.platform
    if base_name.startswith("linux"):
        return Operating_System.linux
    elif base_name.startswith("win"):
        return Operating_System.windows
    elif base_name.startswith("darwin"):
        return Operating_System.macos
    elif base_name.startswith("freebsd"):
        return Operating_System.freebsd
    return None




def assert_argument_value(component, args):
    '''
    Checks whether the given arg/component combo has the right Value
    If the component needs no argument, it will return none
    If an argument is needed but there is a default value, it will return the default
    If the argument is needed but there is no default value it will raise a ValueError
    '''
    if not args:
        if argument_is_optional(component):
            return None
        elif argument_has_default(component):
            return HARDWARE_DEFAULTS[component][1]
        else:
            raise ValueError("Trying to access data without specifying the argument. component: {}"
                             .format(component))
    return args


def check_comp_args(main_dict, component, args=None):
    """
        Performs all necessary assertions and checks on the component metric and args value
        Also checks given main_dict whether the comp exists there

        Returns the proper args if None was given but the comp has a necessary default argument
    """
    assert_component_exists(main_dict, component)

    new_args = assert_argument_value(component, args)

    create_subdict_if_necessary(main_dict, component, new_args)

    return new_args
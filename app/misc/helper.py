"""
    Helper Module to help you through the ups and down of the project
"""

from importlib import import_module
import sys
import os

from misc.constants import HARDWARE_DEFAULTS, Operating_System

APP_FOLDER_NAME = "app"

def import_if_exists(module):
    """ Loads and returns the handle for the given module if it available on the system"""
    try:
        new_module = globals()[module] = import_module(module)
    except ImportError:
        print("{} couldn't be imported'".format(module))
        return None
    else:
        print("{} has been successfully imported".format(module))
        return new_module


def argument_is_optional(hardware):
    """ Checks whether for the given hardware an argument is optional """
    return not HARDWARE_DEFAULTS[hardware][0]


def argument_has_default(hardware):
    """ Checks whether the given hardware has a default argument """
    if HARDWARE_DEFAULTS[hardware][1] != None:
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
    if type(dict_to_test) == type(dict()):
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

def get_path_to_app():
    """
        Returns the absolute path to the app folder of the project
        E.g. /home/opserv/opserv-backend/app
    """
    if not __file__:
        ValueError("__file__ wasn't set.'")

    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Search for parent until arrived at test
    while os.path.basename(current_dir) != APP_FOLDER_NAME:
        if current_dir == os.path.dirname(current_dir): # Top Level of filesystem reached
            FileNotFoundError("Couldn't find app directory'")
        current_dir = os.path.dirname(current_dir) # Get the parent directory of current_dir

    return current_dir

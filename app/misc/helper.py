"""
    Helper Module to help you through the ups and down of the project
"""

import errno
import os
import sys
from importlib import import_module

from misc.constants import HARDWARE_DEFAULTS, Operating_System

APP_FOLDER_NAME = "app"


def import_if_exists(module):
    """ Loads and returns the handle for the given module if it available on the system"""
    try:
        new_module = globals()[module] = import_module(module)
    except ImportError:
        print("{} couldn't be imported'".format(module))  # TODO Exchange with logging
        return None
    else:
        print("{} has been successfully imported".format(module))  # TODO Exchange with logging
        return new_module


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
        if current_dir == os.path.dirname(current_dir):  # Top Level of filesystem reached
            FileNotFoundError("Couldn't find app directory'")
        current_dir = os.path.dirname(current_dir)  # Get the parent directory of current_dir

    return current_dir


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


def is_pathname_valid(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    SRC: http://stackoverflow.com/questions/9532499
    '''
    # Sadly, Python fails to provide the following magic number for us.
    ERROR_INVALID_NAME = 123

    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)  # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            # If an OS-specific exception is raised, its error code
            # indicates whether this pathname is valid or not. Unless this
            # is the case, this exception implies an ignorable kernel or
            # filesystem complaint (e.g., path not found or inaccessible).
            #
            # Only the following exceptions indicate invalid pathnames:
            #
            # * Instances of the Windows-specific "WindowsError" class
            #   defining the "winerror" attribute whose value is
            #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
            #   fine-grained and hence useful than the generic "errno"
            #   attribute. When a too-long pathname is passed, for example,
            #   "errno" is "ENOENT" (i.e., no such file or directory) rather
            #   than "ENAMETOOLONG" (i.e., file name too long).
            # * Instances of the cross-platform "OSError" class defining the
            #   generic "errno" attribute whose value is either:
            #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
            #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError as exc:
        return False
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        return True
        # If any other exception was raised, this is an unrelated fatal issue
        # (e.g., a bug). Permit this exception to unwind the call stack.
        #
        # Did we mention this should be shipped with Python already?

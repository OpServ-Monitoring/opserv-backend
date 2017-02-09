"""
    Standalone helper file that can be used without any other dependencies int
    the software
"""

import errno
import os
import sys
import socket
from importlib import import_module
from urllib.request import urlopen
from urllib.parse import quote, unquote
import logging

log = logging.getLogger("opserv." + __name__)

APP_FOLDER_NAME = "app"


def import_if_exists(module):
    """ Loads and returns the handle for the given module if it available on the system"""
    try:
        new_module = globals()[module] = import_module(module)
    except ImportError:
        log.error("{} couldn't be imported'".format(module))
        return None
    else:
        log.debug("{} has been successfully imported".format(module))
        return new_module


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

        # original version - don't use asserts in production code
        # assert os.path.isdir(root_dirname)  # ...Murphy and her ironclad Law
        # new version
        if not os.path.isdir(root_dirname):  # ...Murphy and her ironclad Law
            raise AssertionError

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


def has_internet_access(host="8.8.8.8", port=53, timeout=3):
    """
    Returns a boolean determined by whether the machine has internet
    access
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    Source: http://stackoverflow.com/a/33117579
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


def get_external_ip():
    '''
        Returns the external i.e. public IP address of this machine as UTF8 string
    '''
    return str(urlopen("https://api.ipify.org").read().decode("utf-8"))


def merge_n_lists(*lists: list) -> list:
    """
    Merges the items of n lists into a single list. Each item is handled and returned as string.
    :param lists: A tuple of lists, to be merged
    :return: A list containing all items once
    """
    merged_items = []

    if len(lists) < 1:
        # TODO error handling
        pass
    elif len(lists) == 2:
        merged_items = lists[0]
    else:
        for a_list in lists:
            merged_items += a_list

    merged_items = map(str, merged_items)

    return list(
        set(merged_items)
    )


def encode_string(string: str):
    if string is None:
        return None

    return quote(string, safe='')


def double_encode_string(string: str):
    return encode_string(encode_string(string))


def decode_string(string: str):
    if string is None:
        return None

    return unquote(string)


def double_decode_string(string: str):
    return decode_string(decode_string(string))

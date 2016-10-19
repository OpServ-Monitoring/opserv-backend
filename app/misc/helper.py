from importlib import import_module
import sys

from misc.constants import HARDWARE_DEFAULTS, Operating_System

def importIfExists(module):
    """ Loads and returns the handle for the given module if it available on the system"""
    try:
        newModule = globals()[module] = import_module(module)
    except ImportError:
        print("{} couldn't be imported'".format(module))
        return None
    else:
        print("{} has been successfully imported".format(module))
        return newModule


def argumentIsOptional(hardware):
    """ Checks whether for the given hardware an argument is optional """
    return not HARDWARE_DEFAULTS[hardware][0]


def argumentHasDefault(hardware):
    """ Checks whether the given hardware has a default argument """
    if HARDWARE_DEFAULTS[hardware][1] != None:
        return True
    return False



def createSubDictIfNecessary(mainDict, hardware, args):
    """ Creates a sub-dictionary for arguments if there isn't already one existing and the arguments is not None"""
    assertIsDict(mainDict)
    
    if args == None:
        return
    if not args in mainDict[hardware]:
        mainDict[hardware][args] = {}

def assertComponentExists(mainDict, hardware):
    """ Simple assert to check if the given hardware exists in the constants and realtime dict """
    if not hardware in mainDict or not hardware in HARDWARE_DEFAULTS:
        raise NotImplementedError(hardware)

def assertIsDict(dictToTest):
    if type(dictToTest) == type(dict()):
        return True
    else:
        raise TypeError("This should be a dict" + str(dictToTest))


def get_operating_system():
    baseName = sys.platform
    if baseName.startswith("linux"):
        return Operating_System.linux
    elif baseName.startswith("win"):
        return Operating_System.windows
    elif baseName.startswith("darwin"):
        return Operating_System.macos
    elif baseName.startswith("freebsd"):
        return Operating_System.freebsd
    return None 

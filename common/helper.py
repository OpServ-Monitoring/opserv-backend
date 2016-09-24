from importlib import import_module

''' 

'''


def importIfExists(module):
    try:
        newModule = globals()[module] = import_module(module)
    except ImportError:
        print("{} couldn't be imported'".format(module))
        return None
    else:
        print("{} has been successfully imported".format(module))
        return newModule

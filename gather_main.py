#
# Main file for the gathering thread
#
# 24.08.2016
#
#

import threading

class GatherThread(threading.Thread):
    def __init__(self):
        print("Initializing GatherThread!")
        threading.Thread.__init__(self)
        return

    def run(self):
        print("Running GatherThread")
        return
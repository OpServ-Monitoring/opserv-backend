#
# Main Web Thread file
#
# 24.08.2016
#
#

import threading

class WebThread(threading.Thread):
    def __init__(self):
        print("Initializing WebThread!")
        threading.Thread.__init__(self)
        return

    def run(self):
        print("Running WebThread")
        return
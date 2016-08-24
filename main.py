#
# Main thread seperation file of the opserv backend
#
# 24.08.2016
#
#

import threading
from gather_main import GatherThread
from web_main import WebThread

def startThreads():
    print("Starting up Web and Gathering Thread")
    webThread = WebThread()
    webThread.daemon = True
    webThread.start()

    gatherThread = GatherThread()
    gatherThread.daemon = True
    gatherThread.start()

if __name__ == '__main__':
    startThreads()

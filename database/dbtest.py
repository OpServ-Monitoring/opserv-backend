from vedis import Vedis
import queueManager

db = Vedis('data.db')


def run_me():
    print(queueManager.realTimeDataQueue.get())

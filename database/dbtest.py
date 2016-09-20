import json
import time
from vedis import Vedis

from database.historical_data_retrieve_dumb import summarize_data


def __current_time_millis():
    return int(time.time() * 1000)


db = Vedis('data.db')


class VedisDB:
    instance = None

    class __VedisDB:
        __millis = None

        def __init__(self, arg):
            self.val = arg

        def __str__(self):
            return repr(self) + self.val

        # should be transaction based
        # - every minute
        def put_measurement(self, hardware, id, measure, value):
            if self.__millis is not None and self.__millis + 1000 < self.__current_time_millis():
                # print("millis vorbei")
                self.__millis = None

                # print("commit transaction")
                db.commit()
                # close transaction

            if self.__millis is None:
                # print("keine millis")
                self.__millis = self.__current_time_millis()

                # print("start transaction")
                db.begin()
                # start transaction

            # do some stuff
            listi = db.List(hardware + ";" + id + ";" + measure)
            listi.append({
                "value": value,
                "timestamp": self.__current_time_millis()
            })

        def get_measurement(self, hardware, id, measure, start, end, limit=30):
            listi = db.List(hardware + ";" + id + ";" + measure)

            newlist = []
            for el in listi:
                el = el.replace("'", "\"")

                jsondict = json.loads(el)
                timestamp = jsondict["timestamp"]

                if start <= timestamp <= end:
                    newlist.append(jsondict)

            if limit >= len(newlist):
                return newlist

            print("limit weniger big")
            return self.__limit(newlist, limit)

        @staticmethod
        def __limit(alist, limit):
            return summarize_data(alist, limit)

        @staticmethod
        def __current_time_millis():
            return int(time.time() * 1000)

    def __init__(self, arg):
        if not VedisDB.instance:
            VedisDB.instance = VedisDB.__VedisDB(arg)
        else:
            VedisDB.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)


db_instance = VedisDB("haha")


def run_me():
    pass
    #  db_instance.put_measurement("cpu", "cpu0", "usage", 25.5)


run_me()

#  print(db_instance.get_measurement("cpu", "cpu0", "usage", 0, __current_time_millis(), 5))

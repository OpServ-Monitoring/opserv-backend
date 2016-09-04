from flask_restful import Resource
import queueManager


class SampleData(Resource):
    def get(self, cpu, cpu_core):
        data = queueManager.realTimeDataQueue.get()

        return {
            'cpu': cpu,
            'cpu-core': cpu_core,
            'usage': data
        }


"""
    /v1/cpu/<id:int>
    /v1/cpu/all
    /v1/cpu/combined
        HEADER:
        start: default 0
        end: default maxint
        limit: default 20

        /realtime
        - keine Header


    hallo.de/api/data/v1/cpu/3?start=215124&end=266235623&limit=50
    hallo.de/api/data/v1/cpu/realtime
"""

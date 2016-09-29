from .cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreUsageEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/usage"
        ]

    @staticmethod
    def get_name():
        return "cpu core usage measurement"

        # TODO Remove - reference only
        # def _get_realtime_data(self):
        #     import queue_manager
        #     import time
        #
        #     queue_manager.requestDataQueue.put({"hardware": "cores", "valueType": "usage"})
        #     queue = queue_manager.getQueue("cores", "usage")
        #
        #     amount = None
        #     while amount is None:
        #         amount = queue.get()
        #         time.sleep(0.02)
        #
        #     data = {
        #         'value': amount,
        #         'unit': 'percent'
        #     }
        #
        #     self._response_holder.set_body_data(data)

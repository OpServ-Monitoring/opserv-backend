from server.restful_api.data.v1.endpoints.cpucores_cpucore__general_child import CpucoresCpucoreGeneralChildEndpoint


class CpucoresCpucoreUsageEndpoint(CpucoresCpucoreGeneralChildEndpoint):
    def _get(self) -> bool:
        # TODO Implement endpoint
        return True

    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/usage"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    def _get_realtime_data(self):
        import queue_manager
        import time

        queue_manager.requestDataQueue.put({"hardware": "cores", "valueType": "usage"})
        queue = queue_manager.getQueue("cores", "usage")

        amount = None
        while amount is None:
            amount = queue.get()
            time.sleep(0.02)

        data = {
            'value': amount,
            'unit': 'percent'
        }

        self._response_holder.set_body_data(data)

    def _get_historical_data(self):
        print('historical', self._start, self._end, self._limit)

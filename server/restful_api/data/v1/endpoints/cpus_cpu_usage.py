from server.restful_api.data.v1.endpoints.cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuUsageEndpoint(CpusCpuGeneralChildEndpoint):
    def _get(self) -> bool:
        print("called with", self._is_realtime)

        if self._is_realtime:
            self._get_realtime_data()
        else:
            pass  # self._get_historical_data()

        return True

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/usage"
        ]

    @staticmethod
    def get_name():
        return "cpu usage measurement"

    @staticmethod
    def _get_children():
        return []

    def _get_realtime_data(self):
        import queue_manager
        import time

        # queue_manager.requestDataQueue.put({"hardware": "cpu", "valueType": "usage"})
        queue = queue_manager.getQueue("cpu", "usage")

        amount = None

        timestamp = time.time()
        amount = queue.get()
        print(time.time() - timestamp)

        data = {
            'value': amount,
            'unit': 'percent'
        }

        self._response_holder.set_body_data(data)

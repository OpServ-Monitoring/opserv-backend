from server.restful_api.data.v1.endpoints.__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpusCpuUsageEndpoint(GeneralEndpointRealtimeHistorical):
    def _get(self):
        if self._is_realtime:
            self._get_realtime_data()
        else:
            pass  # self._get_historical_data()

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/usage"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.endpoints.cpus_cpu import CpusCpuEndpoint

        return CpusCpuEndpoint

    @staticmethod
    def _get_children():
        return []

    def _get_realtime_data(self):
        import queue_manager
        import time

        queue_manager.requestDataQueue.put({"hardware": "cpu", "valueType": "load"})
        queue = queue_manager.getQueue("cpu", "load")

        amount = None
        while amount is None:
            amount = queue.get()
            time.sleep(0.001)

        data = {
            'value': amount,
            'unit': 'percent'
        }

        self._response_holder.set_body_data(data)

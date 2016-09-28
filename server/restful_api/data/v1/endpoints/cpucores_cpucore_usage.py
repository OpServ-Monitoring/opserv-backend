from server.restful_api.data.v1.endpoints.__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpucoresCpucoreUsageEndpoint(GeneralEndpointRealtimeHistorical):
    def _get(self):
        if not ("cpu_core" in self._request_holder.get_params()):
            # TODO Improve error message
            self._response_holder = self._get_bad_request_response(self._response_holder,
                                                                   "The cpu_core value is invalid or missing.")
            return

        if self._is_realtime:
            self._get_realtime_data()
        else:
            self._get_historical_data()

    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>/usage"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.endpoints.cpucores_cpucore import CpucoresCpucoreEndpoint

        return CpucoresCpucoreEndpoint

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

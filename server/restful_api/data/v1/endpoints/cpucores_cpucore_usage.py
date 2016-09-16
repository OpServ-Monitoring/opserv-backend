from server.restful_api.data.v1.endpoints.__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpucoresCpucoreUsageEndpoint(GeneralEndpointRealtimeHistorical):
    def _get(self):
        if not ("cpu_core" in self._request_holder.get_params()):
            # TODO Improve error message
            self._response_holder = self._get_bad_request_response(self._response_holder,
                                                                   "The cpu_core value is invalid or missing.")
            return

        if self._is_realtime:
            self.__on_realtime_action()
        else:
            self.__on_historical_action()

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

    def __on_realtime_action(self):
        print('is realtime')

    def __on_historical_action(self):
        print('historical', self._start, self._end, self._limit)

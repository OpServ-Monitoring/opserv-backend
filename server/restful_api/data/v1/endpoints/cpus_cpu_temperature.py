from server.restful_api.data.v1.endpoints.__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpusCpuTemperatureEndpoint(GeneralEndpointRealtimeHistorical):
    def _get(self):
        if self._is_realtime:
            self.__on_realtime_action()
        else:
            self.__on_historical_action()

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/temperature"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent_name():
        from server.restful_api.data.v1.endpoints.cpus_cpu import CpusCpuEndpoint
        return CpusCpuEndpoint.get_name()

    def _get_children(self):
        return []

    def __on_realtime_action(self):
        print('is realtime')

    def __on_historical_action(self):
        print('historical', self._start, self._end, self._limit)

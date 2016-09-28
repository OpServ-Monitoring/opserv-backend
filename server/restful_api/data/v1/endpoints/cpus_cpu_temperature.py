from server.restful_api.data.v1.endpoints.cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuTemperatureEndpoint(CpusCpuGeneralChildEndpoint):
    def _get(self) -> bool:
        if self._is_realtime:
            self.__on_realtime_action()
        else:
            self.__on_historical_action()

        return True

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/temperature"
        ]

    @staticmethod
    def get_name():
        return "cpu temperature measurement"

    @staticmethod
    def _get_children():
        return []

    def __on_realtime_action(self):
        print('is realtime')

    def __on_historical_action(self):
        print('historical', self._start, self._end, self._limit)

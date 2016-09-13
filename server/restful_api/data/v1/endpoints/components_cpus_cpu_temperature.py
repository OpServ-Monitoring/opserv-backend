import queueManager
from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1
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
            "/components/cpus/<string:cpu>/temperature"
        ]

    def __on_realtime_action(self):
        print('is realtime')

    def __on_historical_action(self):
        print('historical', self._start, self._end, self._limit)

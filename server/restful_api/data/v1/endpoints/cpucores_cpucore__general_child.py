from abc import ABCMeta

from server.restful_api.data.v1.endpoints.__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpucoresCpucoreGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):

    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.endpoints.cpucores_cpucore import CpucoresCpucoreEndpoint

        return CpucoresCpucoreEndpoint

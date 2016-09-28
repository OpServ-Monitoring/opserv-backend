from abc import ABCMeta

from server.restful_api.data.v1.endpoints.__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpucoresCpucoreGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.endpoints.cpucores_cpucore import CpucoresCpucoreEndpoint

        return CpucoresCpucoreEndpoint

    @staticmethod
    def _get_mandatory_parameters():
        from server.restful_api.data.v1.endpoints.cpucores_cpucore import CpucoresCpucoreEndpoint

        return [
            CpucoresCpucoreEndpoint.get_cpucore_id_validator()
        ]

    @staticmethod
    def _get_children():
        return []

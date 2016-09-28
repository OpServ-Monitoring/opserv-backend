from abc import ABCMeta

from server.restful_api.data.v1.endpoints.__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpusCpuGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.endpoints.cpus_cpu import CpusCpuEndpoint

        return CpusCpuEndpoint

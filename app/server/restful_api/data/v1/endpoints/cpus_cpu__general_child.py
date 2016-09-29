from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpusCpuGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from .cpus_cpu import CpusCpuEndpoint

        return CpusCpuEndpoint

    @staticmethod
    def _get_mandatory_parameters():
        from .cpus_cpu import CpusCpuEndpoint

        return [
            CpusCpuEndpoint.get_cpu_id_validator()
        ]

    @staticmethod
    def _get_children():
        return []

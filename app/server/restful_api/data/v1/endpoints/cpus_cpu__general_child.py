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

    def _get_component_type(self) -> str:
        return "cpu"

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["cpu"]

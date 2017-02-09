from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class CpusCpuGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @classmethod
    def _get_parent(cls):
        from .cpus_cpu import CpusCpuEndpoint

        return CpusCpuEndpoint

    @classmethod
    def _get_mandatory_parameters(cls):
        from .cpus_cpu import CpusCpuEndpoint

        return [
            CpusCpuEndpoint.get_cpu_id_validator()
        ]

    @classmethod
    def _get_children(cls):
        return []

    @classmethod
    def _get_component_type(cls) -> str:
        return "cpu"

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["cpu"]

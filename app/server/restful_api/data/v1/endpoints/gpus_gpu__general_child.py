from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class GpusGpuGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @classmethod
    def _get_parent(cls):
        from .gpus_gpu import GpusGpuEndpoint

        return GpusGpuEndpoint

    @classmethod
    def _get_mandatory_parameters(cls):
        from .gpus_gpu import GpusGpuEndpoint

        return [
            GpusGpuEndpoint.get_gpu_id_validator()
        ]

    @classmethod
    def _get_children(cls):
        return []

    def _get_component_type(self) -> str:
        return "gpu"

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["gpu"]

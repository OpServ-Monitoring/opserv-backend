from misc.standalone_helper import decode_string, double_decode_string
from .__general_data_v1 import GeneralEndpointDataV1


class GpusGpuEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        gpu_id = self._request_holder.get_params()["gpu"]
        gpu_id = decode_string(gpu_id)

        persisted_info = self._outbound_gate.get_last_measurement("gpu", gpu_id, "info")

        if persisted_info is not None:
            self._response_holder.update_body_data({
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
            })

        return True

    @classmethod
    def get_paths(cls):
        return [
            "/gpus/<string:gpu>"
        ]

    @classmethod
    def get_name(cls):
        return "gpu entity"

    @classmethod
    def _get_parent(cls):
        from .gpus import GpusEndpoint

        return GpusEndpoint

    @classmethod
    def _get_children(cls):
        from .gpus_gpu_usage import GpusGpuUsageEndpoint
        from .gpus_gpu_gpuclock import GpusGpuGpuclockEndpoint
        from .gpus_gpu_memclock import GpusGpuMemclockEndpoint
        from .gpus_gpu_vramusage import GpusGpuVramusageEndpoint
        from .gpus_gpu_temperature import GpusGpuTemperatureEndpoint

        return [
            ("/usage", GpusGpuUsageEndpoint),
            ("/gpuclock", GpusGpuGpuclockEndpoint),
            ("/memclock", GpusGpuMemclockEndpoint),
            ("/vramusage", GpusGpuVramusageEndpoint),
            ("/temperature", GpusGpuTemperatureEndpoint)
        ]

    @classmethod
    def _get_mandatory_parameters(cls):
        return [
            cls.get_gpu_id_validator()
        ]

    @classmethod
    def get_gpu_id_validator(cls):
        return "gpu", lambda x: cls._outbound_gate.is_argument_valid(
            "gpu", double_decode_string(x))

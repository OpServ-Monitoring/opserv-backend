from .__general_data_v1 import GeneralEndpointDataV1


class GpusGpuEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        # TODO implement endpoint
        from app.database.unified_database_interface import UnifiedDatabaseInterface
        gpu_id = self._request_holder.get_params()["gpu"]

        persisted_info = UnifiedDatabaseInterface.get_measurement_data_reader().get_last_value("gpu", gpu_id, "info")

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info[0],
                "general-info": persisted_info[1]
            })

        return True

    @staticmethod
    def get_paths():
        return [
            "/gpus/<string:gpu>"
        ]

    @staticmethod
    def get_name():
        return "gpu entity"

    @staticmethod
    def _get_parent():
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

    @staticmethod
    def _get_mandatory_parameters():
        return [
            GpusGpuEndpoint.get_gpu_id_validator()
        ]

    @staticmethod
    def get_gpu_id_validator():
        # TODO Validate gpu id
        return "gpu", lambda x: True
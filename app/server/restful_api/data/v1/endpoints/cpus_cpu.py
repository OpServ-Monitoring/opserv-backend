from .__general_data_v1 import GeneralEndpointDataV1


class CpusCpuEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        # TODO implement endpoint
        return True

    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>"
        ]

    @staticmethod
    def get_name():
        return "cpu entity"

    @staticmethod
    def _get_parent():
        from .cpus import CpusEndpoint

        return CpusEndpoint

    @staticmethod
    def _get_children():
        from .cpus_cpu_frequency import CpusCpuFrequencyEndpoint
        from .cpus_cpu_temperature import CpusCpuTemperatureEndpoint
        from .cpus_cpu_usage import CpusCpuUsageEndpoint

        return [
            ("/frequency", CpusCpuFrequencyEndpoint),
            ("/temperature", CpusCpuTemperatureEndpoint),
            ("/usage", CpusCpuUsageEndpoint)
        ]

    @staticmethod
    def _get_mandatory_parameters():
        return [
            CpusCpuEndpoint.get_cpu_id_validator()
        ]

    @staticmethod
    def get_cpu_id_validator():
        # TODO Validate cpu id
        return "cpu", lambda x: int(x) > 4

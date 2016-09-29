from .__general_data_v1 import GeneralEndpointDataV1


class CpucoresCpucoreEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        # TODO implement endpoint
        return True

    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:cpu_core>"
        ]

    @staticmethod
    def get_name():
        return "cpu core entity"

    @staticmethod
    def _get_parent():
        from .cpucores import CpucoresEndpoint

        return CpucoresEndpoint

    @staticmethod
    def _get_children():
        from .cpucores_cpucore_frequency import CpucoresCpucoreFrequencyEndpoint
        from .cpucores_cpucore_temperature import CpucoresCpucoreTemperatureEndpoint
        from .cpucores_cpucore_usage import CpucoresCpucoreUsageEndpoint

        return [
            ("/frequency", CpucoresCpucoreFrequencyEndpoint),
            ("/temperature", CpucoresCpucoreTemperatureEndpoint),
            ("/usage", CpucoresCpucoreUsageEndpoint)
        ]

    @staticmethod
    def _get_mandatory_parameters():
        return [
            CpucoresCpucoreEndpoint.get_cpucore_id_validator()
        ]

    @staticmethod
    def get_cpucore_id_validator():
        # TODO Validate cpucore id
        return "cpu_core", lambda x: int(x) > 4

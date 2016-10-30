from .__general_data_v1 import GeneralEndpointDataV1


class CpucoresCpucoreEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        # TODO implement endpoint
        from app.database.unified_database_interface import UnifiedDatabaseInterface
        cpu_core_id = self._request_holder.get_params()["core"]

        persisted_info = UnifiedDatabaseInterface.get_measurement_data_reader().get_last_value("core", cpu_core_id,
                                                                                               "info")

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info[0],
                "general-info": persisted_info[1]
            })

        return True

    @staticmethod
    def get_paths():
        return [
            "/cpu-cores/<string:core>"
        ]

    @staticmethod
    def get_name():
        return "cpu core entity"

    @staticmethod
    def _get_parent():
        from .cpucores import CpucoresEndpoint

        return CpucoresEndpoint

    @classmethod
    def _get_children(cls):
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
        return "core", lambda x: True

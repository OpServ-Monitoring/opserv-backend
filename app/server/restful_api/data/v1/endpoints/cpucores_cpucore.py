from misc.standalone_helper import decode_string, double_decode_string
from .__general_data_v1 import GeneralEndpointDataV1


class CpucoresCpucoreEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        cpu_core_id = self._request_holder.get_params()["cpu_core"]
        cpu_core_id = decode_string(cpu_core_id)

        persisted_info = self._outbound_gate.get_last_measurement("cpucore", cpu_core_id, "info")
        if persisted_info is not None:
            self._response_holder.update_body_data({
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
            })

        return True

    @classmethod
    def get_paths(cls):
        return [
            "/cpu-cores/<string:cpu_core>"
        ]

    @classmethod
    def get_name(cls):
        return "cpu core entity"

    @classmethod
    def _get_parent(cls):
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

    @classmethod
    def _get_mandatory_parameters(cls):
        return [
            cls.get_cpucore_id_validator()
        ]

    @classmethod
    def get_cpucore_id_validator(cls):
        return "cpu_core", lambda x: cls._outbound_gate.is_argument_valid(
            "cpucore", double_decode_string(x))

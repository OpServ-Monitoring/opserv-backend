from server.data_gates.default_data_gate import DefaultDataGate
from .__general_data_v1 import GeneralEndpointDataV1


class CpusCpuEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        cpu_id = self._request_holder.get_params()["cpu"]

        persisted_info = DefaultDataGate.get_last_measurement("cpu", cpu_id, "info")

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info[0],
                "general-info": persisted_info[1]
            })

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

    @classmethod
    def _get_children(cls):
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
        return "cpu", lambda x: DefaultDataGate.is_argument_valid(x, "cpus")

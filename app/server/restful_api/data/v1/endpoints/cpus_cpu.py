from .__general_data_v1 import GeneralEndpointDataV1


class CpusCpuEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        cpu_id = self._request_holder.get_params()["cpu"]

        persisted_info = self._outbound_gate.get_last_measurement("cpu", "info", cpu_id)

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
            })

        return True

    @classmethod
    def get_paths(cls):
        return [
            "/cpus/<string:cpu>"
        ]

    @classmethod
    def get_name(cls):
        return "cpu entity"

    @classmethod
    def _get_parent(cls):
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

    @classmethod
    def _get_mandatory_parameters(cls):
        return [
            cls.get_cpu_id_validator()
        ]

    @classmethod
    def get_cpu_id_validator(cls):
        from server.data_gates.default_data_gate import DefaultDataGate
        return "cpu", lambda x: cls._outbound_gate.is_argument_valid(
            DefaultDataGate.decode_argument(DefaultDataGate.decode_argument(x)), "cpu")

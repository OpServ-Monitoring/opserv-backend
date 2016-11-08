from .__general_data_v1 import GeneralEndpointDataV1


class ProcessesProcessEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        process_id = self._request_holder.get_params()["process"]

        persisted_info = self._outbound_gate.get_last_measurement("process", "info", process_id)

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
            })

        return True

    @staticmethod
    def get_paths():
        return [
            "/processes/<string:process>"
        ]

    @staticmethod
    def get_name():
        return "process entity"

    @staticmethod
    def _get_parent():
        from .processes import ProcessesEndpoint

        return ProcessesEndpoint

    @classmethod
    def _get_children(cls):
        from .processes_process_cpuusage import ProcessesProcessCpuusageEndpoint
        from .processes_process_memusage import ProcessesProcessMemusageEndpoint
        from .processes_process_name import ProcessesProcessNameEndpoint

        return [
            ("/cpuusage", ProcessesProcessCpuusageEndpoint),
            ("/memusage", ProcessesProcessMemusageEndpoint),
            ("/name", ProcessesProcessNameEndpoint)
        ]

    @staticmethod
    def _get_mandatory_parameters():
        return [
            ProcessesProcessEndpoint.get_process_id_validator()
        ]

    @classmethod
    def get_process_id_validator(cls):
        return "process", lambda x: cls._outbound_gate.is_argument_valid(x, "processes")

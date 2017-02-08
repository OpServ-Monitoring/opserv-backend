from .__general_data_v1 import GeneralEndpointDataV1


class ProcessesProcessEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        process_id = self._request_holder.get_params()["process"]

        persisted_info = self._outbound_gate.get_last_measurement("process", "info", process_id)

        general_information = {}
        if persisted_info is not None:
            general_information = {
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
            }

        pid = None
        process_name = None

        # TODO Improve the pid/name extraction
        # EXTRACTION START
        from urllib.parse import unquote
        raw_process_information = unquote(process_id)

        import re
        matches = re.match("([^:]+):(.+)", raw_process_information)
        if matches is not None:
            pid = matches.group(1)
            process_name = matches.group(2)
        # EXTRACTION END

        self._response_holder.set_body_data({
            "information": general_information,
            "pid": pid,
            "process_name": process_name
        })

        return True

    @classmethod
    def get_paths(cls):
        return [
            "/processes/<string:process>"
        ]

    @classmethod
    def get_name(cls):
        return "process entity"

    @classmethod
    def _get_parent(cls):
        from .processes import ProcessesEndpoint

        return ProcessesEndpoint

    @classmethod
    def _get_children(cls):
        from .processes_process_cpuusage import ProcessesProcessCpuusageEndpoint
        from .processes_process_memusage import ProcessesProcessMemusageEndpoint

        return [
            ("/cpuusage", ProcessesProcessCpuusageEndpoint),
            ("/memusage", ProcessesProcessMemusageEndpoint)
        ]

    @classmethod
    def _get_mandatory_parameters(cls):
        return [
            cls.get_process_id_validator()
        ]

    @classmethod
    def get_process_id_validator(cls):
        from server.data_gates.default_data_gate import DefaultDataGate
        return "process", lambda x: cls._outbound_gate.is_argument_valid(
            DefaultDataGate.decode_argument(DefaultDataGate.decode_argument(x)), "process")

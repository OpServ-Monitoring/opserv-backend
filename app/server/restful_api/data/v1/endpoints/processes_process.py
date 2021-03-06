from misc.standalone_helper import decode_string, double_decode_string
from .__general_data_v1 import GeneralEndpointDataV1


class ProcessesProcessEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        process_id = self._request_holder.get_params()["process"]
        process_id = decode_string(process_id)

        persisted_info = self._outbound_gate.get_last_measurement("process", process_id, "info")

        general_information = {}
        if persisted_info is not None:
            general_information = {
                "timestamp": persisted_info["timestamp"],
                "general-info": persisted_info["value"]
            }

        pid = None
        process_name = None

        # TODO Future version: Improve the pid/name extraction
        # EXTRACTION START
        raw_process_information = decode_string(process_id)

        import re
        matches = re.match("([^:]+):(.+)", raw_process_information)
        if matches is not None:
            pid = matches.group(1)
            process_name = matches.group(2)
        # EXTRACTION END

        self._response_holder.update_body_data({
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
        return "process", lambda x: cls._outbound_gate.is_argument_valid(
            "process", double_decode_string(x))

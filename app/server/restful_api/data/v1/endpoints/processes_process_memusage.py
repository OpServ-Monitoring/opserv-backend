from .processes_process__general_child import ProcessesProcessGeneralChildEndpoint


class ProcessesProcessMemusageEndpoint(ProcessesProcessGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/processes/<string:process>/memusage"
        ]

    @classmethod
    def get_name(cls):
        return "process memory usage measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "memusage"

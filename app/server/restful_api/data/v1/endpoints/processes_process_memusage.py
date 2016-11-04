from .processes_process__general_child import ProcessesProcessGeneralChildEndpoint


class ProcessesProcessMemusageEndpoint(ProcessesProcessGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/processes/<string:process>/memusage"
        ]

    @staticmethod
    def get_name():
        return "process memory usage measurement"

    def _get_component_metric(self) -> str:
        return "memusage"

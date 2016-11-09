from .processes_process__general_child import ProcessesProcessGeneralChildEndpoint


class ProcessesProcessNameEndpoint(ProcessesProcessGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/processes/<string:process>/name"
        ]

    @classmethod
    def get_name(cls):
        return "process name measurement"

    def _get_component_metric(self) -> str:
        return "name"

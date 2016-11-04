from .processes_process__general_child import ProcessesProcessGeneralChildEndpoint


class ProcessesProcessNameEndpoint(ProcessesProcessGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/processes/<string:process>/name"
        ]

    @staticmethod
    def get_name():
        return "process name measurement"

    def _get_component_metric(self) -> str:
        return "name"

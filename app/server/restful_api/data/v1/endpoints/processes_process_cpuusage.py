from .processes_process__general_child import ProcessesProcessGeneralChildEndpoint


class ProcessesProcessCpuusageEndpoint(ProcessesProcessGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/processes/<string:process>/cpuusage"
        ]

    @staticmethod
    def get_name():
        return "process cpu usage measurement"

    def _get_component_metric(self) -> str:
        return "cpuusage"

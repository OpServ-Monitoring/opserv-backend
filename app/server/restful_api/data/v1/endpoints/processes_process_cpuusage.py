from .processes_process__general_child import ProcessesProcessGeneralChildEndpoint


class ProcessesProcessCpuusageEndpoint(ProcessesProcessGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/processes/<string:process>/cpuusage"
        ]

    @classmethod
    def get_name(cls):
        return "process cpu usage measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "cpuusage"

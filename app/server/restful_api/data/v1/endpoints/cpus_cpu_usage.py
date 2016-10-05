from .cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuUsageEndpoint(CpusCpuGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/usage"
        ]

    @staticmethod
    def get_name():
        return "cpu usage measurement"

    def _get_component_metric(self) -> str:
        return "usage"

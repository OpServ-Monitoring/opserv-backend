from .cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuUsageEndpoint(CpusCpuGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/cpus/<string:cpu>/usage"
        ]

    @classmethod
    def get_name(cls):
        return "cpu usage measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "usage"

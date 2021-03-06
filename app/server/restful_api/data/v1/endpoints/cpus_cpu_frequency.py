from .cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuFrequencyEndpoint(CpusCpuGeneralChildEndpoint):
    @classmethod
    def get_paths(cls):
        return [
            "/cpus/<string:cpu>/frequency"
        ]

    @classmethod
    def get_name(cls):
        return "cpu frequency measurement"

    @classmethod
    def _get_component_metric(cls) -> str:
        return "frequency"

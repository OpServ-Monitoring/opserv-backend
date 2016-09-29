from .cpus_cpu__general_child import CpusCpuGeneralChildEndpoint


class CpusCpuFrequencyEndpoint(CpusCpuGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpus/<string:cpu>/frequency"
        ]

    @staticmethod
    def get_name():
        return "cpu frequency measurement"

from .data_api_v1_endpoint import DataApiV1Endpoint
from .endpoints.cpucores import CpucoresEndpoint
from .endpoints.cpucores_cpucore import CpucoresCpucoreEndpoint
from .endpoints.cpucores_cpucore_frequency import CpucoresCpucoreFrequencyEndpoint
from .endpoints.cpucores_cpucore_temperature import CpucoresCpucoreTemperatureEndpoint
from .endpoints.cpucores_cpucore_usage import CpucoresCpucoreUsageEndpoint
from .endpoints.cpus import CpusEndpoint
from .endpoints.cpus_cpu import CpusCpuEndpoint
from .endpoints.cpus_cpu_frequency import CpusCpuFrequencyEndpoint
from .endpoints.cpus_cpu_temperature import CpusCpuTemperatureEndpoint
from .endpoints.cpus_cpu_usage import CpusCpuUsageEndpoint
from .endpoints.gpus import GpusEndpoint
from .endpoints.gpus_gpu import GpusGpuEndpoint
from ...general.endpoint_management import EndpointManagement


class EndpointManagementDataV1(EndpointManagement):
    @staticmethod
    def get_prefix():
        return "/v1"

    @staticmethod
    def get_endpoints():
        return [
            DataApiV1Endpoint,  # /v1

            # - - - CPU - - - #

            CpusEndpoint,  # /v1/cpus
            CpusCpuEndpoint,  # /v1/cpus/<string:cpu>
            CpusCpuUsageEndpoint,  # /v1/cpus/<string:cpu>/usage
            CpusCpuTemperatureEndpoint,  # /v1/cpus/<string:cpu>/temperature
            CpusCpuFrequencyEndpoint,  # /v1/cpus/<string:cpu>/frequency


            # - - - CPU CORES - - - #

            CpucoresEndpoint,  # /v1/cpu-cores
            # /v1/cpus/<string:cpu>/cpu-cores
            CpucoresCpucoreEndpoint,  # /v1/cpu-cores/<string:cpu_core>
            # /v1/cpus/<string:cpu>/cpu-cores/<string:cpu_core>
            CpucoresCpucoreUsageEndpoint,  # /v1/cpu-cores/<string:cpu_core>/usage
            # /v1/cpus/<string:cpu>/cpu-cores/<string:cpu_core>/usage
            CpucoresCpucoreTemperatureEndpoint,  # /v1/cpu-cores/<string:cpu_core>/temperature
            # /v1/cpus/<string:cpu>/cpu-cores/<string:cpu_core>/temperature
            CpucoresCpucoreFrequencyEndpoint,  # /v1/cpu-cores/<string:cpu_core>/frequency
            # /v1/cpus/<string:cpu>/cpu-cores/<string:cpu_core>/frequency


            # - - - GPU - - - #

            GpusEndpoint,  # v1/gpus
            GpusGpuEndpoint,  # v1/gpus/<string:gpu>
            # v1/gpus/<string:gpu>/gpu-clock
            # v1/gpus/<string:gpu>/memory-clock
            # v1/gpus/<string:gpu>/vram-usage
            # v1/gpus/<string:gpu>/temperature
            # v1/gpus/<string:gpu>/usage

            # - - - RAM - - - #

            # v1/ram
            # v1/ram/used-memory
            # v1/ram/total-memory

        ]


"""
    Processes
    Filesystem / HDD
"""

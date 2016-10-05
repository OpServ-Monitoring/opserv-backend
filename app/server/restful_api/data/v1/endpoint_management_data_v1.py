from app.server.restful_api.data.v1.endpoints.gpus_gpu_gpuclock import GpusGpuGpuclockEndpoint
from app.server.restful_api.data.v1.endpoints.gpus_gpu_memclock import GpusGpuMemclockEndpoint
from app.server.restful_api.data.v1.endpoints.gpus_gpu_temperature import GpusGpuTemperatureEndpoint
from app.server.restful_api.data.v1.endpoints.gpus_gpu_usage import GpusGpuUsageEndpoint
from app.server.restful_api.data.v1.endpoints.gpus_gpu_vramusage import GpusGpuVramusageEndpoint
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
            CpucoresCpucoreEndpoint,  # /v1/cpu-cores/<string:cpu_core>
            CpucoresCpucoreUsageEndpoint,  # /v1/cpu-cores/<string:cpu_core>/usage
            CpucoresCpucoreTemperatureEndpoint,  # /v1/cpu-cores/<string:cpu_core>/temperature
            CpucoresCpucoreFrequencyEndpoint,  # /v1/cpu-cores/<string:cpu_core>/frequency

            # - - - GPU - - - #

            GpusEndpoint,  # v1/gpus
            GpusGpuEndpoint,  # v1/gpus/<string:gpu>
            GpusGpuGpuclockEndpoint,  # v1/gpus/<string:gpu>/gpuclock
            GpusGpuMemclockEndpoint,  # v1/gpus/<string:gpu>/memclock
            GpusGpuTemperatureEndpoint,  # v1/gpus/<string:gpu>/temperature
            GpusGpuUsageEndpoint,  # v1/gpus/<string:gpu>/usage
            GpusGpuVramusageEndpoint  # v1/gpus/<string:gpu>/vramusage

            # - - - RAM - - - #

            # v1/ram
            # v1/ram/used-memory
            # v1/ram/total-memory

        ]


"""
    Processes
    Filesystem / HDD
"""

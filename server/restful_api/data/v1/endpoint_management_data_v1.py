from server.restful_api.data.v1.endpoints.components_cpucores_cpucore import CpucoresCpucoreEndpoint
from server.restful_api.data.v1.endpoints.components_cpucores_cpucore_frequency import CpucoresCpucoreFrequencyEndpoint
from server.restful_api.data.v1.endpoints.components_cpucores_cpucore_info import CpucoresCpucoreInfoEndpoint
from server.restful_api.data.v1.endpoints.components_cpucores_cpucore_temperature import \
    CpucoresCpucoreTemperatureEndpoint
from server.restful_api.data.v1.endpoints.components_cpus import CpusEndpoint
from server.restful_api.data.v1.endpoints.components_cpus_cpu import CpusCpuEndpoint
from server.restful_api.data.v1.endpoints.components_cpus_cpu_frequency import CpusCpuFrequencyEndpoint
from server.restful_api.data.v1.endpoints.components_cpus_cpu_info import CpusCpuInfoEndpoint
from server.restful_api.data.v1.endpoints.components_cpus_cpu_temperature import CpusCpuTemperatureEndpoint
from server.restful_api.data.v1.endpoints.components_cpus_cpu_usage import CpusCpuUsageEndpoint
from server.restful_api.data.v1.endpoints.overview import OverviewEndpoint
from server.restful_api.data.v1.endpoints.components_cpucores_cpucore_usage import CpucoresCpucoreUsageEndpoint
from server.restful_api.data.v1.endpoints.components_cpucores import CpucoresEndpoint
from server.restful_api.data.v1.endpoints.compontents import ComponentsEndpoint
from server.restful_api.general.endpoint_management import EndpointManagement


class EndpointManagementDataV1(EndpointManagement):

    @staticmethod
    def get_prefix():
        return "/v1"

    @staticmethod
    def get_endpoints():
        return [
            OverviewEndpoint,                       # /v1
            ComponentsEndpoint,                     # /v1/components


            # - - - CPU - - - #

            CpusEndpoint,                           # /v1/components/cpu
            CpusCpuEndpoint,                        # /v1/components/cpu/<string:cpu>
            CpusCpuUsageEndpoint,                   # /v1/components/cpu/<string:cpu>/usage
            CpusCpuTemperatureEndpoint,             # /v1/components/cpu/<string:cpu>/temperature
            CpusCpuInfoEndpoint,                    # /v1/components/cpu/<string:cpu>/info
            CpusCpuFrequencyEndpoint,               # /v1/components/cpu/<string:cpu>/frequency


            # - - - CPU CORES - - - #

            CpucoresEndpoint,                       # /v1/components/cpu-cores
                                                    # /v1/components/cpu/<string:cpu>/cpu-cores
            CpucoresCpucoreEndpoint,                # /v1/components/cpu-cores/<string:cpu_core>
                                                    # /v1/components/cpu/<string:cpu>/cpu-cores/<string:cpu_core>
            CpucoresCpucoreUsageEndpoint,           # /v1/components/cpu-cores/<string:cpu_core>/usage
                                                    # /v1/components/cpu/<string:cpu>/cpu-cores/<string:cpu_core>/usage
            CpucoresCpucoreTemperatureEndpoint,     # /v1/components/cpu-cores/<string:cpu_core>/temperature
                                                    # /v1/components/cpu/<string:cpu>/cpu-cores/<string:cpu_core>/temperature
            CpucoresCpucoreInfoEndpoint,            # /v1/components/cpu-cores/<string:cpu_core>/info
                                                    # /v1/components/cpu/<string:cpu>/cpu-cores/<string:cpu_core>/info
            CpucoresCpucoreFrequencyEndpoint        # /v1/components/cpu-cores/<string:cpu_core>/frequency
                                                    # /v1/components/cpu/<string:cpu>/cpu-cores/<string:cpu_core>/frequency


            # - - - GPU - - - #

            # v1/components/gpu
            # v1/components/gpu/<string:gpu>
            # v1/components/gpu/<string:gpu>/info
            # v1/components/gpu/<string:gpu>/gpu-clock
            # v1/components/gpu/<string:gpu>/memory-clock
            # v1/components/gpu/<string:gpu>/vram-usage
            # v1/components/gpu/<string:gpu>/temperature
            # v1/components/gpu/<string:gpu>/usage


            # - - - RAM - - - #

            # v1/components/ram
            # v1/components/ram/used-memory
            # v1/components/ram/total-memory



        ]


"""
    Processes
    Filesystem / HDD
"""

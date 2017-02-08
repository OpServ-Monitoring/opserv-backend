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
from .endpoints.disks import DisksEndpoint
from .endpoints.disks_disk import DisksDiskEndpoint
from .endpoints.disks_disk_status import DisksDiskStatusEndpoint
from .endpoints.disks_disk_temperature import DisksDiskTemperatureEndpoint
from .endpoints.disks_disk_usage import DisksDiskUsageEndpoint
from .endpoints.gatheringrates import GatheringRatesEndpoint
from .endpoints.gpus import GpusEndpoint
from .endpoints.gpus_gpu import GpusGpuEndpoint
from .endpoints.gpus_gpu_gpuclock import GpusGpuGpuclockEndpoint
from .endpoints.gpus_gpu_memclock import GpusGpuMemclockEndpoint
from .endpoints.gpus_gpu_temperature import GpusGpuTemperatureEndpoint
from .endpoints.gpus_gpu_usage import GpusGpuUsageEndpoint
from .endpoints.gpus_gpu_vramusage import GpusGpuVramusageEndpoint
from .endpoints.memory import MemoryEndpoint
from .endpoints.memory_free import MemoryFreeEndpoint
from .endpoints.memory_total import MemoryTotalEndpoint
from .endpoints.memory_used import MemoryUsedEndpoint
from .endpoints.networks import NetworksEndpoint
from .endpoints.networks_network import NetworksNetworkEndpoint
from .endpoints.networks_network_receivepersec import NetworksNetworkReceivepersecEndpoint
from .endpoints.networks_network_transmitpersec import \
    NetworksNetworkTransmitpersecEndpoint
from .endpoints.partitions import PartitionsEndpoint
from .endpoints.partitions_partition import PartitionsPartitionEndpoint
from .endpoints.partitions_partition_free import PartitionsPartitionFreeEndpoint
from .endpoints.partitions_partition_total import PartitionsPartitionTotalEndpoint
from .endpoints.partitions_partition_used import PartitionsPartitionUsedEndpoint
from .endpoints.processes import ProcessesEndpoint
from .endpoints.processes_process import ProcessesProcessEndpoint
from .endpoints.processes_process_cpuusage import ProcessesProcessCpuusageEndpoint
from .endpoints.processes_process_memusage import ProcessesProcessMemusageEndpoint
from .endpoints.system import SystemEndpoint
from .endpoints.system_cpucores import SystemCpucoresEndpoint
from .endpoints.system_cpus import SystemCpusEndpoint
from .endpoints.system_disks import SystemDisksEndpoint
from .endpoints.system_gpus import SystemGpusEndpoint
from .endpoints.system_networks import SystemNetworksEndpoint
from .endpoints.system_partitions import SystemPartitionsEndpoint
from .endpoints.system_processes import SystemProcessesEndpoint
from ...general.endpoint_management import EndpointManagement


class EndpointManagementDataV1(EndpointManagement):
    @classmethod
    def get_prefix(cls):
        return "/v1"

    @classmethod
    def get_endpoints(cls):
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
            GpusGpuVramusageEndpoint,  # v1/gpus/<string:gpu>/vramusage

            # - - - RAM - - - #
            MemoryEndpoint,  # v1/memory
            MemoryFreeEndpoint,  # v1/memory/free
            MemoryTotalEndpoint,  # v1/memory/total
            MemoryUsedEndpoint,  # v1/memory/used

            # - - - DISK - - - #
            DisksEndpoint,  # v1/disks
            DisksDiskEndpoint,  # v1/disks/<string:disk>
            DisksDiskStatusEndpoint,  # v1/disks/<string:disk>/status
            DisksDiskTemperatureEndpoint,  # v1/disks/<string:disk>/temperature
            DisksDiskUsageEndpoint,  # v1/disks/<string:disk>/usage

            # - - - NETWORK - - - #
            NetworksEndpoint,  # v1/networks
            NetworksNetworkEndpoint,  # v1/networks/<string:network>
            NetworksNetworkReceivepersecEndpoint,  # v1/networks/<string:network>/receivepersec
            NetworksNetworkTransmitpersecEndpoint,  # v1/networks/<string:network>/transmitpersec

            # - - - PARTITION - - - #
            PartitionsEndpoint,  # v1/partitions
            PartitionsPartitionEndpoint,  # v1/partitions/<string:partition>
            PartitionsPartitionFreeEndpoint,  # v1/partitions/<string:partition>/free
            PartitionsPartitionTotalEndpoint,  # v1/partitions/<string:partition>/total
            PartitionsPartitionUsedEndpoint,  # v1/partitions/<string:partition>/used

            # - - - PROCESS - - - #
            ProcessesEndpoint,  # v1/processes
            ProcessesProcessEndpoint,  # v1/processes/<string:process>
            ProcessesProcessCpuusageEndpoint,  # v1/processes/<string:process>/cpuusage
            ProcessesProcessMemusageEndpoint,  # v1/processes/<string:process>/memusage

            # # - - - SYSTEM - - - #
            SystemEndpoint,  # v1/system
            SystemCpucoresEndpoint,  # v1/system/cpu-cores
            SystemCpusEndpoint,  # v1/system/cpus
            SystemDisksEndpoint,  # v1/system/disks
            SystemGpusEndpoint,  # v1/system/gpus
            SystemNetworksEndpoint,  # v1/system/networks
            SystemPartitionsEndpoint,  # v1/system/partitions
            SystemProcessesEndpoint,  # v1/system/processes

            # # - - - GATHERING RATES - - - #
            GatheringRatesEndpoint
        ]

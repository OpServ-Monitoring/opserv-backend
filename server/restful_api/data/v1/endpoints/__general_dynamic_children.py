from abc import ABCMeta

from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class GeneralEndpointDynamicChildren(GeneralEndpointDataV1, metaclass=ABCMeta):
    def _get(self):
        pass

    def _get_children(self):
        from server.restful_api.data.v1.endpoints.cpus_cpu import CpusCpuEndpoint

        children = []

        ids = []  # self.__get_children_ids()
        for cpu_id in ids:
            children.append(("/" + cpu_id, CpusCpuEndpoint))

        return children

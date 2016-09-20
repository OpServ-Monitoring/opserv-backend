from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpucoresEndpoint(GeneralEndpointDataV1):
    def _get(self):
        # TODO general info
        pass

    @staticmethod
    def get_paths():
        return [
            "/cpu-cores"
        ]

    @staticmethod
    def get_name():
        # TODO change name
        return "CHANGE ME"

    @staticmethod
    def _get_parent():
        from server.restful_api.data.v1.data_api_v1_endpoint import DataApiV1Endpoint

        return DataApiV1Endpoint

    def _get_children(self):
        from server.restful_api.data.v1.endpoints.cpucores_cpucore import CpucoresCpucoreEndpoint

        children = []

        ids = self.__get_children_ids()
        for child_id in ids:
            children.append(("/" + child_id, CpucoresCpucoreEndpoint))

        return children

    def __get_children_ids(self):
        # TODO Implement dynamic children
        import queue_manager
        import time

        queue_manager.requestDataQueue.put({"hardware": "system", "valueType": "cores"})
        queue = queue_manager.getQueue("system", "cores")

        amount = None
        while amount is None:
            amount = queue.get()
            time.sleep(0.02)

        children_ids = []
        if amount is not None:
            for i in range(0, amount):
                children_ids.append(str(i))

        return children_ids

from server.restful_api.data.v1.endpoints.root__general_child import RootGeneralChildEndpoint


class CpusEndpoint(RootGeneralChildEndpoint):
    def _get(self) -> bool:
        # no data section available
        return self.KEEP_PROCESSING()

    @staticmethod
    def get_paths():
        return [
            "/cpus"
        ]

    @staticmethod
    def get_name():
        return "cpu entities"

    @staticmethod
    def _get_children():
        from server.restful_api.data.v1.endpoints.cpus_cpu import CpusCpuEndpoint

        children = []

        ids = CpusEndpoint.__get_children_ids()
        for child_id in ids:
            children.append(("/" + child_id, CpusCpuEndpoint))

        return children

    @staticmethod
    def __get_children_ids():
        # TODO Implement dynamic children
        import queue_manager
        import time

        queue_manager.requestDataQueue.put({"hardware": "system", "valueType": "cpus"})
        queue = queue_manager.getQueue("system", "cpus")

        amount = None
        while amount is None:
            amount = queue.get()
            time.sleep(0.02)

        children_ids = []
        if amount is not None:
            for i in range(0, amount):
                children_ids.append(str(i))

        return children_ids

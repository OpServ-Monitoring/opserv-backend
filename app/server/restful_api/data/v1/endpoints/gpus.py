from .root__general_child import RootGeneralChildEndpoint


class GpusEndpoint(RootGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/gpus"
        ]

    @staticmethod
    def get_name():
        return "gpu entities"

    @staticmethod
    def _get_children():
        from .gpus_gpu import GpusGpuEndpoint

        children = []

        ids = GpusEndpoint.__get_children_ids()
        for child_id in ids:
            children.append(("/" + child_id, GpusGpuEndpoint))

        return children

    @staticmethod
    def __get_children_ids():
        # TODO Implement dynamic children
        import queue_manager
        import time

        queue_manager.requestDataQueue.put({"hardware": "system", "valueType": "gpus"})
        queue = queue_manager.getQueue("system", "gpus")

        amount = None
        while amount is None:
            amount = queue.get()
            time.sleep(0.02)

        children_ids = []
        if amount is not None:
            for i in range(0, amount):
                children_ids.append(str(i))

        return children_ids

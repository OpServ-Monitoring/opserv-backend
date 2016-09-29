from .root__general_child import RootGeneralChildEndpoint


class CpucoresEndpoint(RootGeneralChildEndpoint):
    @staticmethod
    def get_paths():
        return [
            "/cpu-cores"
        ]

    @staticmethod
    def get_name():
        return "cpu core entities"

    @staticmethod
    def __get_children_ids():
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

    @staticmethod
    def _get_children():
        from .cpucores_cpucore import CpucoresCpucoreEndpoint
        children = []

        ids = CpucoresEndpoint.__get_children_ids()
        for child_id in ids:
            children.append(("/" + child_id, CpucoresCpucoreEndpoint))

        return children

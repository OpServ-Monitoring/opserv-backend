import abc


class EndpointManagement:
    @staticmethod
    @abc.abstractmethod
    def get_endpoints():
        return []

    @staticmethod
    @abc.abstractmethod
    def get_prefix():
        return ""

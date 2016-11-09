from abc import abstractmethod


class EndpointManagement:
    @classmethod
    @abstractmethod
    def get_endpoints(cls):
        return []

    @classmethod
    @abstractmethod
    def get_prefix(cls):
        return ""

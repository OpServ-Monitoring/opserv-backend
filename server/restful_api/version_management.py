import abc


class VersionManagement:
    __api = None
    __base_api_path = None
    __is_current = False
    __version = None

    def __init__(self, api, base_api_path, is_current=False):
        self.__api = api
        self.__base_api_path = base_api_path
        self.__is_current = is_current

        self.__version = self._get_version_path()

    @abc.abstractmethod
    def add_version_to_api(self):
        # abstract method that every subclass should implement to add endpoints using __add_endpoint_to_api()
        return

    def _add_endpoint_to_api(self, endpoint, resource):
        paths = self.__get_api_paths(endpoint)

        self.__api.add_resource(resource, *paths)

    def __get_api_paths(self, endpoint):
        paths = [self.__base_api_path + self.__version + endpoint]

        if self.__is_current:
            paths.append(self.__base_api_path + "/current" + endpoint)

        return tuple(paths)

    @abc.abstractmethod
    def _get_version_path(self):
        # abstract method that every subclass should implement to return its version path
        return

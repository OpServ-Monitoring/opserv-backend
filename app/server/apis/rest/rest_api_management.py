from server.apis.rest.preferences.endpoint_preference import EndpointPreference
from server.apis.rest.preferences.endpoint_preferences import EndpointPreferences
from .data.endpoint_api_root import EndpointApiRoot
from .data.endpoint_component import EndpointComponent
from .data.endpoint_component_metric import EndpointComponentMetric
from .data.endpoint_component_type import EndpointComponentType
from .users.endpoint_user import EndpointUser
from .users.endpoint_users import EndpointUsers
from .._api_management import ApiManagement


class RestApiManagement(ApiManagement):
    @classmethod
    def _get_api_prefix(cls) -> str:
        return "/rest/v1"

    @classmethod
    def _get_handlers(cls) -> list:
        handlers = [
            ("/*", None)  # TODO Add handler that lists /data, /config, /users, /preferences
        ]

        handlers.extend(cls.__get_config_handlers())
        handlers.extend(cls.__get_data_handlers())
        handlers.extend(cls.__get_preference_handlers())
        handlers.extend(cls.__get_users_handlers())

        return handlers

    @classmethod
    def __get_config_handlers(cls) -> list:
        config_handlers = []

        return cls.add_prefix_to_handlers("/config", config_handlers)

    @classmethod
    def __get_data_handlers(cls) -> list:
        data_handlers = [
            ("/*", EndpointApiRoot),
            ("/([^/]+)/*", EndpointComponentType),
            ("/([^/]+)/([^/]+)/*", EndpointComponent),
            ("/([^/]+)/([^/]+)/([^/]+)/*", EndpointComponentMetric)
        ]

        return cls.add_prefix_to_handlers("/data", data_handlers)

    @classmethod
    def __get_preference_handlers(cls) -> list:
        preference_handlers = [
            ("/*", EndpointPreferences),
            ("/([^/]+)/*", EndpointPreference)
        ]

        return cls.add_prefix_to_handlers("/preferences", preference_handlers)

    @classmethod
    def __get_users_handlers(cls) -> list:
        users_handlers = [
            ("/*", EndpointUsers),
            ("/([^/]+)/*", EndpointUser)
        ]

        return cls.add_prefix_to_handlers("/users", users_handlers)

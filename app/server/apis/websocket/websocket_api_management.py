from .websocket_handler import WebsocketHandler
from .._api_management import ApiManagement


class WebsocketApiManagement(ApiManagement):
    @classmethod
    def _get_api_prefix(cls) -> str:
        return "/websocket/v1"

    @classmethod
    def _get_handlers(cls) -> list:
        return [
            ("/*", WebsocketHandler)
        ]

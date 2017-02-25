from server.apis.auth.endpoint_authenticate import EndpointAuthenticate
from server.apis.auth.endpoint_renew_token import EndpointRenewToken
from .._api_management import ApiManagement


class AuthApiManagement(ApiManagement):
    @classmethod
    def _get_api_prefix(cls) -> str or None:
        return "/auth"

    @classmethod
    def _get_handlers(cls) -> list:
        return [
            ("/*", EndpointAuthenticate),
            ("/renew/*", EndpointRenewToken)
        ]

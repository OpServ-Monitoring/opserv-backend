from misc.standalone_helper import double_encode_string
from ..preferences_api_versions_endpoint import PreferencesApiVersionsEndpoint
from ...general.endpoint import Endpoint


# TODO Future version: Add doc strings for the http methods


class PreferencesApiV1Endpoint(Endpoint):
    def _put(self) -> bool:
        self._response_holder.set_bad_request_response(
            'HTTP method PUT is not supported by this resource'
        )

        return False

    def _post(self) -> bool:
        self._response_holder.set_bad_request_response(
            'HTTP method POST is not supported by this resource'
        )

        return False

    def _delete(self) -> bool:
        self._response_holder.set_bad_request_response(
            'HTTP method DELETE is not supported by this resource'
        )

        return False

    def _post_process(self) -> bool:
        return True

    @classmethod
    def _get_parent(cls):
        return PreferencesApiVersionsEndpoint

    def _get(self) -> bool:
        # no data section available
        return self.KEEP_PROCESSING()

    @classmethod
    def get_paths(cls):
        return [""]

    @classmethod
    def get_name(cls):
        return "preferences API v1 entry"

    @classmethod
    def _get_children(cls):
        from server.restful_api.preferences.v1.preference import PreferenceEndpoint
        keys_in_use = cls._outbound_gate.get_user_preference_keys()

        children = []
        for key in keys_in_use:
            key = double_encode_string(key)

            children.append(
                ("/" + key, PreferenceEndpoint)
            )

        return children

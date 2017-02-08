from ..preferences_api_versions_endpoint import PreferencesApiVersionsEndpoint
from ...general.endpoint import Endpoint


# TODO fix all docs for http methods, return type is no longer the ResponseHolder


class PreferencesApiV1Endpoint(Endpoint):
    def _put(self) -> bool:
        """
        The PUT-method is not supported by this api version, thus an response indicating a bad request is returned
        :return: A ResponseHolder holding a response with the bad request code
        """
        self._set_bad_request_response(
            'HTTP method PUT is not supported by this resource'
        )

        return False

    def _post(self) -> bool:
        """
        The POST-method is not supported by this api version, thus an response indicating a bad request is returned
        :return: A ResponseHolder holding a response with the bad request code
        """
        self._set_bad_request_response(
            'HTTP method POST is not supported by this resource'
        )

        return False

    def _delete(self) -> bool:
        """
        The DELETE-method is not supported by this api version, thus an response indicating a bad request is returned
        :return: A ResponseHolder holding a response with the bad request code
        """
        self._set_bad_request_response(
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
        from database.unified_database_interface import UnifiedDatabaseInterface  # TODO Exchange with data gate
        from server.restful_api.preferences.v1.preference import PreferenceEndpoint

        keys_in_use = UnifiedDatabaseInterface.get_user_preferences_writer_reader().get_used_user_preference_keys()  # TODO Exchange with data gate

        children = []
        for key in keys_in_use:
            from server.data_gates.default_data_gate import DefaultDataGate
            key = DefaultDataGate.double_encode_argument(key)

            children.append(
                ("/" + key, PreferenceEndpoint)
            )

        return children

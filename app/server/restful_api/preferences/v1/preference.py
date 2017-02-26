import json

from misc.standalone_helper import decode_string
from .preferences_api_v1_endpoint import PreferencesApiV1Endpoint
from ...general.endpoint import Endpoint


class PreferenceEndpoint(Endpoint):
    def _get(self) -> bool:
        pref_key = self._request_holder.get_params()["pref_key"]
        pref_key = decode_string(pref_key)

        user_pref = self._outbound_gate.get_user_preference_value(pref_key)

        user_pref_value = None
        if user_pref is not None:
            user_pref_value = json.loads(user_pref)

        self._response_holder.update_body_data({
            "key": pref_key,
            "value": user_pref_value
        })

        return True

    def _put(self) -> bool:
        pref_key = self._request_holder.get_params()["pref_key"]
        pref_key = decode_string(pref_key)

        pref_value = self._request_holder.get_body()["value"]

        self._outbound_gate.set_user_preference(
            pref_key,
            json.dumps(pref_value)
        )

        self._response_holder.update_body_data({
            "key": pref_key,
            "value": pref_value
        })

        return True

    def _post(self) -> bool:
        """
                The POST-method is not supported by this api version, thus an response indicating a bad request is returned
                :return: A ResponseHolder holding a response with the bad request code
                """
        self._response_holder.set_bad_request_response(
            'HTTP method POST is not supported by this resource'
        )
        return False

    def _delete(self) -> bool:
        pref_key = self._request_holder.get_params()["pref_key"]
        pref_key = decode_string(pref_key)

        self._outbound_gate.delete_user_preference(pref_key)

        self._response_holder.update_body_data({
            "message": "preference " + pref_key + " deleted."
        })

        return True

    @classmethod
    def _get_children(cls) -> list:
        return []

    @classmethod
    def get_paths(cls):
        return [
            "/<string:pref_key>"
        ]

    def _post_process(self) -> bool:
        return True

    @classmethod
    def _get_parent(cls):
        return PreferencesApiV1Endpoint

    @classmethod
    def get_name(cls):
        return "preference"

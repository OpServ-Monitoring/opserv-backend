import json

import tornado.escape
import tornado.web

from server.apis.authenticated_endpoint import AuthenticatedEndpoint


class EndpointPreference(AuthenticatedEndpoint):
    def get(self, preference_key):
        user_pref = self.__get_preference_by_key(preference_key)

        if user_pref is not None:
            user_pref_value = tornado.escape.json_decode(user_pref)

            data = self.get_resource_object(
                "preference",
                preference_key,
                value=user_pref_value
            )

            self.respond(data)

    def delete(self, preference_key):
        user_pref = self.__get_preference_by_key(preference_key)

        if user_pref is not None:
            self._outbound_gate.delete_user_preference()

    def patch(self, preference_key):
        user_pref = self.__get_preference_by_key(preference_key)
        request_body = self.__get_parsed_request_body()

        if user_pref is not None and request_body is not None and "value" in request_body:
            updated_value = request_body["value"]

            self._outbound_gate.set_user_preference(
                preference_key,
                tornado.escape.json_encode(updated_value)
            )

            # TODO Return updated dataset

    def __get_parsed_request_body(self):
        try:
            return tornado.escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError:
            self.send_error(400)  # TODO Add details - body not formatted correctly

    def __get_preference_by_key(self, preference_key):
        preference = self._outbound_gate.get_user_preference(preference_key)

        if preference is None:
            pass  # self.send_error(400)  # TODO Add details
        return preference

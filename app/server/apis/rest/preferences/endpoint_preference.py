import json
import logging

import tornado.escape
import tornado.web

from server.apis.authenticated_endpoint import AuthenticatedEndpoint

log = logging.getLogger("opserv." + __name__)


class EndpointPreference(AuthenticatedEndpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "GET")
        self.add_header("Allow", "DELETE")
        self.add_header("Allow", "PATCH")
        self.add_header("Allow", "PUT")

    def get(self, preference_key):
        if preference_key in self._outbound_gate.get_user_preference_keys():
            preference_value = self._outbound_gate.get_user_preference_value(preference_key)

            try:
                preference_value = tornado.escape.json_decode(preference_value)
            except json.JSONDecodeError:
                log.debug("Tried to decode the following as JSON string but will be returned as is: '{0}'".format(
                    preference_value
                ))

            data = self.get_resource_object(
                "preference",
                preference_key,
                {
                    "value": preference_value
                }
            )

            self.respond(data)
        else:
            self.__send_error_non_existing_preference_key(preference_key)

    def delete(self, preference_key):
        if preference_key in self._outbound_gate.get_user_preference_keys():
            self._outbound_gate.delete_user_preference(preference_key)
        else:
            self.__send_error_non_existing_preference_key(preference_key)

    def patch(self, preference_key):
        if preference_key in self._outbound_gate.get_user_preference_keys():
            self.__create_or_update_preference(preference_key)
        else:
            self.__send_error_non_existing_preference_key(preference_key)

    def put(self, preference_key):
        if preference_key not in self._outbound_gate.get_user_preference_keys():
            self.__create_or_update_preference(preference_key)
        else:
            self.send_error(
                400,
                **{
                    "summary": "preference key does exist already",
                    "details": "A preference with the specified preference_key '{0}' does exist already. "
                               "You may change a existing preference with the PATCH method.".format(preference_key)
                }
            )

    def __create_or_update_preference(self, preference_key: str):
        request_body = self.__get_parsed_request_body()

        if request_body is not None and "value" in request_body:
            self._outbound_gate.set_user_preference(
                preference_key,
                tornado.escape.json_encode(request_body["value"])
            )
        else:
            self.__send_error_preference_value_missing()

    def __send_error_non_existing_preference_key(self, preference_key):
        self.send_error(
            400,
            **{
                "summary": "preference key does not exist",
                "details": "A preference with the specified preference_key '{0}' does not exist. "
                           "You may add a preference with the PUT method.".format(preference_key)
            }
        )

    def __send_error_preference_value_missing(self):
        self.send_error(
            400,
            **{
                "summary": "preference value missing",
                "details": "You need to specify a \"value\" to use inside the request body."
            }
        )

    def __get_parsed_request_body(self):
        try:
            return tornado.escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError:
            self.send_error(
                400,
                **{
                    "summary": "request body not formatted correctly",
                    "details": "The request body has to be a valid JSON object or array."
                }
            )

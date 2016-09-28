from abc import ABCMeta

from server.restful_api.general.endpoint import Endpoint


class GeneralEndpointDataV1(Endpoint, metaclass=ABCMeta):
    def _pre_process(self):
        return super(GeneralEndpointDataV1, self)._pre_process() and self.__includes_mandatory_parameters()

    def __includes_mandatory_parameters(self):
        mandatory_parameters = self._get_mandatory_parameters()

        if mandatory_parameters is not None:
            for mandatory_parameter in mandatory_parameters:
                parameter_name = mandatory_parameter[0]
                verification_function = mandatory_parameter[1]

                actual_value = self._request_holder.get_params()[parameter_name]
                if actual_value is None:
                    self._set_bad_request_response("parameter " + parameter_name + " missing.")

                    return False
                elif verification_function is None or not callable(verification_function):
                    self._set_internal_server_error_response()

                    return False
                elif not verification_function(actual_value):
                    self._set_bad_request_response("parameter " + parameter_name + " is not properly formatted.")

                    return False

        return True

    def _post_process(self):
        response_headers = self._response_holder.get_response_headers()

        response_headers['Access-Control-Allow-Origin'] = '*'
        response_headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response_headers['Access-Control-Allow-Methods'] = 'GET'

        self._response_holder.set_response_headers(response_headers)

        return True

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

    @staticmethod
    def _get_mandatory_parameters():
        return []

from abc import ABCMeta

from ....general.endpoint import Endpoint


class GeneralEndpointDataV1(Endpoint, metaclass=ABCMeta):
    def _pre_process(self):
        keep_processing = super(GeneralEndpointDataV1, self)._pre_process()

        mandatory_parameters = self._get_mandatory_parameters()
        if keep_processing and mandatory_parameters is not None:
            keep_processing = self.__are_mandatory_parameters_valid(mandatory_parameters)

        return keep_processing

    def __are_mandatory_parameters_valid(self, mandatory_parameters):
        for mandatory_parameter in mandatory_parameters:
            if not self.__is_mandatory_parameter_valid(mandatory_parameter):
                return False

        return True

    def __is_mandatory_parameter_valid(self, mandatory_parameter):
        parameter_name = mandatory_parameter[0]
        verification_function = mandatory_parameter[1]

        params = self._request_holder.get_params()

        if params is None or parameter_name not in params:
            self._set_bad_request_response("parameter " + parameter_name + " missing.")
        else:
            actual_value = params[parameter_name]

            if verification_function is None or not callable(verification_function):
                self._set_internal_server_error_response()
            elif not verification_function(actual_value):
                self._set_bad_request_response("parameter " + parameter_name + " is not properly formatted.")
            else:
                return True
        return False

    # TODO Remove this as PUTs are now supported (to set gathering rates) or keep this and simply override the needed endpoints
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

    def _post_process(self):
        response_headers = self._response_holder.get_response_headers()

        response_headers['Access-Control-Allow-Origin'] = '*'
        response_headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response_headers['Access-Control-Allow-Methods'] = 'GET'

        self._response_holder.set_response_headers(response_headers)

        return True

    # TODO Simply check if key exists - DataGate
    @classmethod
    def _get_mandatory_parameters(cls):
        return []

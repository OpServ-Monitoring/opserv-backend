class ResponseHolder:
    __body = {}
    __status = 200
    __response_headers = {}

    def __init__(self, body=None, status=200, headers=None):
        if body is None:
            body = {}
        self.__body = body

        self.__status = status

        if headers is None:
            headers = {}
        self.__response_headers = headers

    def get_body(self):
        return self.__body

    def get_body_data(self):
        return self.__body['data']

    def get_status(self):
        return self.__status

    def get_response_headers(self):
        return self.__response_headers

    def set_body(self, body):
        self.__body = body

    def update_body_data(self, data):
        old_data = self.__body['data']

        if old_data is None:
            old_data = {}

        new_data = old_data.copy()
        new_data.update(data)

        self.__body['data'] = new_data

    def set_status(self, status):
        self.__status = status

    def set_response_headers(self, headers):
        self.__response_headers = headers

    def add_response_headers(self, headers):
        self.__response_headers.update(headers)

    def set_fault_response(self, status_code, error_message):
        """
        helper method to set an error response
        :param status_code: The http status code the response should have
        :param error_message: The error message to display as part of the response
        :return: None
        """
        self.set_body(
            {
                "error_message": error_message
            }
        )
        self.set_status(status_code)

    def set_bad_request_response(self, error_message=None):
        """
        helper method to set a bad request response
        :param error_message: The error_message to display
        :return: None
        """
        if error_message is None:
            error_message = "Bad Request"

        self.set_fault_response(400, error_message)

    def set_internal_server_error_response(self):
        """
        helper method to set a internal server error response
        :return: None
        """
        self.set_fault_response(500, "Internal server error")

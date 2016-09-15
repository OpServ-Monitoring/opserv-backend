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

    def get_status(self):
        return self.__status

    def get_response_headers(self):
        return self.__response_headers

    def set_body(self, body):
        self.__body = body

    def set_status(self, status):
        self.__status = status

    def set_response_headers(self, headers):
        self.__response_headers = headers

    def add_response_headers(self, headers):
        self.__response_headers.update(headers)

class RequestHolder:
    __http_method = None
    __request_headers = None
    __params = None
    __body = None

    def __init__(self, http_method=None, headers=None, params=None, body=None):
        self.__http_method = http_method
        self.__request_headers = headers
        self.__params = params
        self.__body = body

    @staticmethod
    def METHOD_GET():
        return 0

    @staticmethod
    def METHOD_POST():
        return 1

    @staticmethod
    def METHOD_PUT():
        return 2

    @staticmethod
    def METHOD_DELETE():
        return 3

    def get_http_method(self):
        return self.__http_method

    def get_request_headers(self):
        return self.__request_headers

    def get_params(self):
        return self.__params

    def get_body(self):
        return self.__body

    def set_http_method(self, http_method):
        self.__http_method = http_method

    def set_request_headers(self, headers):
        self.__request_headers = headers

    def set_params(self, params):
        self.__params = params

    def set_body(self, body):
        self.__body = body

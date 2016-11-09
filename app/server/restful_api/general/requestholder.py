class RequestHolder:
    __uri = None
    __http_method = None
    __request_headers = None
    __params = None
    __body = None

    def __init__(self, uri=None, http_method=None, headers=None, params=None, body=None):
        self.__uri = uri
        self.__http_method = http_method
        self.__request_headers = headers
        self.__params = params
        self.__body = body

    @classmethod
    def METHOD_GET(cls):
        return 0

    @classmethod
    def METHOD_POST(cls):
        return 1

    @classmethod
    def METHOD_PUT(cls):
        return 2

    @classmethod
    def METHOD_DELETE(cls):
        return 3

    def get_uri(self):
        return self.__uri

    def get_http_method(self):
        return self.__http_method

    def get_request_headers(self):
        return self.__request_headers

    def get_params(self):
        return self.__params

    def get_body(self):
        return self.__body

    def set_uri(self, uri):
        self.__uri = uri

    def set_http_method(self, http_method):
        self.__http_method = http_method

    def set_request_headers(self, headers):
        self.__request_headers = headers

    def set_params(self, params):
        self.__params = params

    def set_body(self, body):
        self.__body = body

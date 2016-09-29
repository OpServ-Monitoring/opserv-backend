from unittest import TestCase

from app.server.restful_api.general.endpoint import Endpoint


class TestEndpoint(TestCase):
    def test_handle_request(self):
        pass # self.fail()

    def test__pre_process(self):
        pass # self.fail()

    def test__set_bad_request_response(self):
        pass # self.fail()

    def test__set_internal_server_error_response(self):
        pass # self.fail()

    def test_KEEP_PROCESSING(self):
        endpoint = Endpoint()

        self.assertTrue(endpoint.KEEP_PROCESSING())

    def test_STOP_PROCESSING(self):
        endpoint = Endpoint()

        self.assertFalse(endpoint.STOP_PROCESSING())

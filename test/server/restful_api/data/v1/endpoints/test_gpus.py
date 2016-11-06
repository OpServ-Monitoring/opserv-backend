from unittest import TestCase

from server.restful_api.data.v1.endpoints.gpus import GpusEndpoint
from server.restful_api.general.requestholder import RequestHolder
from base_mock_outbound_gate import BaseMockOutboundGate


class TestGpusEndpoint(TestCase):
    def setUp(self):
        self.endpoint = GpusEndpoint()
        self.endpoint.set_outbound_gate(BaseMockOutboundGate)

        self.request = RequestHolder()
        self.request.set_uri("opserv.org/test/api/data/v1/gpus")

    def test_get_paths(self):
        self.assertEqual(
            self.endpoint.get_paths(),
            ["/gpus"]
        )

    def test_get_name(self):
        self.assertEqual(
            self.endpoint.get_name(),
            "gpu entities"
        )

    def test_handle_request_with_method_post(self):
        self.request.set_http_method(RequestHolder.METHOD_POST())

        response = self.endpoint.handle_request(self.request)
        self.assertEqual(
            response.get_status(),
            400
        )

    def test_handle_request_with_method_put(self):
        self.request.set_http_method(RequestHolder.METHOD_PUT())

        response = self.endpoint.handle_request(self.request)
        self.assertEqual(
            response.get_status(),
            400
        )

    def test_handle_request_with_method_delete(self):
        self.request.set_http_method(RequestHolder.METHOD_DELETE())

        response = self.endpoint.handle_request(self.request)
        self.assertEqual(
            response.get_status(),
            400
        )

    def test_handle_request_with_method_get(self):
        self.request.set_http_method(RequestHolder.METHOD_GET())
        response = self.endpoint.handle_request(self.request)

        self.assertEqual(
            response.get_status(),
            200
        )

        response_body = response.get_body()
        self.assertIn(
            "links",
            response_body
        )

        response_body_links = response_body["links"]
        self.assertIn(
            "self",
            response_body_links,
        )

        self.assertIn(
            "parent",
            response_body_links
        )

        self.assertIn(
            "children",
            response_body_links
        )

        self.assertEqual(
            len(response_body_links["children"]),
            2
        )

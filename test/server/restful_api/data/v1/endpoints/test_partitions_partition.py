from unittest import TestCase

from base_mock_outbound_gate import BaseMockOutboundGate

from server.restful_api.data.v1.endpoints.partitions_partition import PartitionsPartitionEndpoint
from server.restful_api.general.requestholder import RequestHolder


class TestPartitionsPartition(TestCase):
    def setUp(self):
        class MockEndpoint(PartitionsPartitionEndpoint):
            _outbound_gate = BaseMockOutboundGate

        self.endpoint = MockEndpoint()

        self.request = RequestHolder()
        self.request.set_uri("opserv.org/test/api/data/v1/partitions/id")
        self.request.set_params({
            "partition": "id"
        })

    def test_get_cpu_id_validator(self):
        validator = self.endpoint.get_partition_id_validator()

        self.assertEqual(
            validator[0],
            "partition"
        )

        validation_func = validator[1]

        self.assertTrue(
            validation_func("id")
        )

        self.assertTrue(
            validation_func("2")
        )

        self.assertFalse(
            validation_func(2)
        )

        self.assertFalse(
            validation_func("")
        )

        self.assertFalse(
            validation_func(None)
        )

    def test_get_name(self):
        self.assertEqual(
            self.endpoint.get_name(),
            "partition entity"
        )

    def test_get_paths(self):
        self.assertEqual(
            self.endpoint.get_paths(),
            ["/partitions/<string:partition>"]
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

    def test_handle_request_with_method_get_and_invalid_params(self):
        self.request.set_http_method(RequestHolder.METHOD_GET())
        self.request.set_params({
            "partition": None
        })

        response = self.endpoint.handle_request(self.request)
        self.assertEqual(
            response.get_status(),
            400
        )

    def test_handle_request_with_method_get_and_without_params(self):
        self.request.set_http_method(RequestHolder.METHOD_GET())
        self.request.set_params({})

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
            3
        )

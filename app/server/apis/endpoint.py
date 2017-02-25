import json
import traceback

import tornado.web
import tornado.escape

from misc import standalone_helper
from server.data_gates.default_data_gate import DefaultDataGate


class Endpoint(tornado.web.RequestHandler):
    _outbound_gate = DefaultDataGate

    def set_default_headers(self):
        super().set_default_headers()

        self.set_header("Content-Type", "application/vnd.api+json")
        self.set_header("Allow", "HEAD")

    def head(self, *args, **kwargs):
        pass

    def respond(self, data):
        path = self.get_path()

        self.write(
            tornado.escape.json_encode({
                "data": data,
                "links": {
                    "self": path
                }
            })
        )

    def get_path(self):
        path = self.request.protocol + "://" + self.request.host + self.request.uri
        if path.endswith("/"):
            path = path[:-1]

        return path

    @classmethod
    def get_resource_object(cls, resource_type: str, resource_id: str, **kwargs):
        data = {
            "type": resource_type,
            "id": resource_id
        }

        if kwargs is not None:
            data["attributes"] = kwargs

    @classmethod
    def get_resource_reference(cls, resource_type: str, resource_id: str, parent_path: str):
        encoded_id = standalone_helper.encode_string(resource_id)

        return {
            "type": resource_type,
            "id": resource_id,
            "links": {
                "self": parent_path + "/" + encoded_id
            }
        }

    # Overrides write_error of it's base class to append the stacktrace in debug mode
    # and additional error information if passed as "summary" and/or "details" into kwargs
    def write_error(self, status_code, **kwargs):
        if "summary" in kwargs and kwargs["summary"] is not None:
            if self._reason is None:
                self._reason = ""
            self._reason += " - "
            self._reason += kwargs["summary"]

        error = {
            "status": status_code,
            "title": self._reason,
        }

        if "details" in kwargs and kwargs["details"] is not None:
            error["detail"] = kwargs["details"]

        # in debug mode, try to append the error trace
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            error_trace = []

            for line in traceback.format_exception(*kwargs["exc_info"]):
                error_trace.append(line)

            error["meta"] = error_trace

        response = {
            "errors": [
                error
            ]
        }

        self.finish(tornado.escape.json_encode(response))

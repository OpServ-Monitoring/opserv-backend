import queueManager
from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class CpucoresCpucoreUsageEndpoint(GeneralEndpointDataV1):
    def _get(self):
        if not ("cpu_core" in self._request_holder.get_params()):
            # TODO Improve error message
            self._response_holder = self._return_bad_request_response(self._response_holder,
                                                               "The cpu_core value is invalid or missing.")
            return

        headers = self._request_holder.get_request_headers()
        if "realtime" in headers and headers["realtime"] == "true":
            self._real_time_data_action()
        elif "start" in headers and headers["start"].isdigit() and "end" in headers and headers["end"].isdigit():
            self.__historical_data_action_with_limit()
        else:
            # TODO Improve error message
            self._response_holder = self._return_bad_request_response(self._response_holder,
                                                               "The request is missing some headers. Ensure that you "
                                                               "either set the header realtime=true or valid values "
                                                               "for the headers start and end")

    def __historical_data_action_with_limit(self):
        request_headers = self._request_holder.get_request_headers()

        start = request_headers["start"]
        end = request_headers["end"]

        limit = 20
        if "limit" in request_headers and request_headers["limit"].isdigit():
            wanted_limit = int(request_headers["limit"])

            if wanted_limit >= 1:
                if wanted_limit > 5000:
                    limit = 5000
                else:
                    limit = wanted_limit

        self._historical_data_action(
            start,
            end,
            limit
        )

    def _real_time_data_action(self):
        # TODO implement
        data = None
        while data is None:
            data = queueManager.realTimeDataQueue.get()

            if not ("hardware" in data and data["hardware"] == "cpu"):
                data = None

        print("data", data)

        self._response_holder.set_body({
            'usage': data["value"]
        })

    def _historical_data_action(self, start, end, limit):
        # TODO implement
        print("historical", start, end, limit)

        self._response_holder.set_body({
            "hello2": "world2",
            "hello3": "world3"
        })

    @staticmethod
    def get_paths():
        return [
            "/components/cpus/<string:cpu>/cpu-cores/<string:cpu_core>/usage",
            "/components/cpu-cores/<string:cpu_core>/usage"
        ]

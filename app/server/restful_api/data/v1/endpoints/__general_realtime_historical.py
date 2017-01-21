import time
from abc import ABCMeta

from server.restful_api.data.v1.endpoints.__general_gathering_metric import GeneralGatheringMetricEndpoint


class GeneralEndpointRealtimeHistorical(GeneralGatheringMetricEndpoint, metaclass=ABCMeta):
    def __init__(self):
        super(GeneralEndpointRealtimeHistorical, self).__init__()

        self._is_realtime = False
        self._start = None
        self._end = None
        self._limit = None

    def _pre_process(self):
        # Check for mandatory parameters
        keep_processing = super(GeneralGatheringMetricEndpoint, self)._pre_process()

        if keep_processing:
            self.__read_headers()

        return keep_processing

    def _get(self):
        keep_processing = super(GeneralEndpointRealtimeHistorical, self)._get()

        if keep_processing:
            if self._is_realtime:
                return self._get_realtime_data()
            else:
                return self._get_historical_data()
        else:
            return self.STOP_PROCESSING()

    def _get_realtime_data(self):
        # TODO Improve method

        component_type = self._get_component_type()
        component_arg = self._get_component_arg()
        component_metric = self._get_component_metric()

        realtime_data = self._outbound_gate.get_last_measurement(component_type, component_metric, component_arg)

        # TODO FIX ERROR - realtime_data could be NONE!
        realtime_data.update({
            "unit": None
        })

        self._response_holder.set_body_data(realtime_data)

        return self.KEEP_PROCESSING()

    def _get_historical_data(self):
        historical_data = self._outbound_gate.get_measurements(
            self._get_component_type(),
            self._get_component_arg(),
            self._get_component_metric(),
            self._start,
            self._end,
            self._limit
        )

        self._response_holder.set_body_data({
            "values": historical_data,
            "unit": None
        })

        return self.KEEP_PROCESSING()

    def __read_headers(self):
        headers = self._request_holder.get_request_headers()

        self.__read_realtime_header(headers)

        if not self._is_realtime:
            self.__read_history_headers(headers)

    def __read_realtime_header(self, headers):
        self._is_realtime = "realtime" in headers and headers["realtime"] == "true"

    def __read_history_headers(self, headers):
        self.__read_start_header(headers)
        self.__read_end_header(headers)
        self.__read_limit_header(headers)

    def __read_start_header(self, headers):
        if "start" in headers and headers["start"].isdigit():
            start = int(headers["start"])

            if start > 0:
                self._start = start

    def __read_end_header(self, headers):
        if "end" in headers and headers["end"].isdigit():
            end = int(headers["end"])

            if end > self._start:
                self._end = end

    def __read_limit_header(self, headers):
        if "limit" in headers and headers["limit"].isdigit():
            limit = int(headers["limit"])

            if 0 < limit <= 5000:
                self._limit = limit
            elif limit > 5000:
                self._limit = 5000

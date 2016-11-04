import time
from abc import ABCMeta, abstractmethod

from server.data_gates.default_data_gate import DefaultDataGate

from .__general_data_v1 import GeneralEndpointDataV1


class GeneralEndpointRealtimeHistorical(GeneralEndpointDataV1, metaclass=ABCMeta):
    def __init__(self):
        super(GeneralEndpointRealtimeHistorical, self).__init__()

        self._is_realtime = False
        self._start = 0
        self._end = int(time.time() * 1000)
        self._limit = 50

    def _pre_process(self):
        # Check for mandatory parameters
        keep_processing = super(GeneralEndpointRealtimeHistorical, self)._pre_process()

        if keep_processing:
            self.__read_headers()

        return keep_processing

    def _get(self):
        if self._is_realtime:
            return self._get_realtime_data()
        else:
            return self._get_historical_data()

    def _get_realtime_data(self):
        # TODO Improve method

        component_type = self._get_component_type()
        component_arg = self._get_component_arg()
        component_metric = self._get_component_metric()

        self._response_holder.set_body_data(
            DefaultDataGate.get_last_measurement(component_type, component_metric, component_arg)
        )

        return True

    def _get_historical_data(self):
        self._response_holder.set_body_data(
            DefaultDataGate.get_measurements(
                self._get_component_type(),
                self._get_component_metric(),
                self._get_component_arg(),
                self._start,
                self._end,
                self._limit
            )
        )

        return True

    def __parse_history_results(self, query_result: list) -> dict:
        parsed_response = {
            'values': [],
            'unit': None
        }

        for row in query_result:
            parsed_response["values"].append(
                {
                    'timestamp': row[3],
                    'min': row[4],
                    'avg': row[5],
                    'max': row[6]
                }
            )

        return parsed_response

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

    @classmethod
    def _get_children(cls):
        return []

    @abstractmethod
    def _get_component_type(self) -> str:
        pass

    @abstractmethod
    def _get_component_arg(self) -> str:
        return "default"

    @abstractmethod
    def _get_component_metric(self) -> str:
        pass

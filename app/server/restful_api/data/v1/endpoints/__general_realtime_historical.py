import time
from abc import ABCMeta, abstractmethod

from database.unified_database_interface import UnifiedDatabaseInterface
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

        from misc import data_manager
        data = data_manager.getMeasurement(component=component_type, args=component_arg, metric=component_metric)
        self._response_holder.set_body_data(data)

        return True

    # TODO Make this a @abstractmethod or generalize it
    def _get_historical_data(self):
        raw_historical_results = UnifiedDatabaseInterface.get_min_avg_max(
            self._get_component_type(),
            self._get_component_arg(),
            self._get_component_metric(),
            self._start,
            self._end,
            float(self._limit)
        )

        parsed_historical_results = self.__parse_history_results(raw_historical_results)

        self._response_holder.set_body_data(
            parsed_historical_results
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

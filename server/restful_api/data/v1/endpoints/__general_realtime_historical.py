import abc
import time

from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class GeneralEndpointRealtimeHistorical(GeneralEndpointDataV1):
    _is_realtime = False
    _start = 0
    _end = int(time.time() * 1000)
    _limit = 50

    def _pre_process(self):
        super(GeneralEndpointRealtimeHistorical, self)._pre_process()

        headers = self._request_holder.get_request_headers()

        self._is_realtime = "realtime" in headers and headers["realtime"] == "true"

        if not self._is_realtime:
            if "start" in headers and headers["start"].isdigit():
                start = int(headers["start"])

                if start > 0:
                    self._start = start

            if "end" in headers and headers["end"].isdigit():
                end = int(headers["end"])

                if end > self._start:
                    self._end = end

            if "limit" in headers and headers["limit"].isdigit():
                limit = int(headers["limit"])

                if limit > 0:
                    if limit < 5000:
                        self._limit = limit
                    else:
                        self._limit = 5000

    @abc.abstractmethod
    def _get(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_paths():
        return []

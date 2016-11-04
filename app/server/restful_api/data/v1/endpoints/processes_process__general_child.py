from abc import ABCMeta

from .__general_realtime_historical import GeneralEndpointRealtimeHistorical


class ProcessesProcessGeneralChildEndpoint(GeneralEndpointRealtimeHistorical, metaclass=ABCMeta):
    @staticmethod
    def _get_parent():
        from .processes_process import ProcessesProcessEndpoint

        return ProcessesProcessEndpoint

    @staticmethod
    def _get_mandatory_parameters():
        from .processes_process import ProcessesProcessEndpoint

        return [
            ProcessesProcessEndpoint.get_process_id_validator()
        ]

    @classmethod
    def _get_children(cls):
        return []

    def _get_component_type(self) -> str:
        return "process"

    def _get_component_arg(self) -> str:
        return self._request_holder.get_params()["process"]

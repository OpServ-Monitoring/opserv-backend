from .__general_data_v1 import GeneralEndpointDataV1


class MemoryEndpoint(GeneralEndpointDataV1):
    def _get(self) -> bool:
        # TODO implement endpoint
        from app.database.unified_database_interface import UnifiedDatabaseInterface

        persisted_info = UnifiedDatabaseInterface.get_measurement_data_reader().get_last_value("memory", "default",
                                                                                               "info")

        if persisted_info is not None:
            self._response_holder.set_body_data({
                "timestamp": persisted_info[0],
                "general-info": persisted_info[1]
            })

        return True

    @staticmethod
    def get_paths():
        return [
            "/memory"
        ]

    @staticmethod
    def get_name():
        return "memory entity"

    @staticmethod
    def _get_parent():
        from ...data_api_versions_endpoint import DataApiVersionsEndpoint

        return DataApiVersionsEndpoint

    @classmethod
    def _get_children(cls):
        # TODO children

        return [
        ]

    @staticmethod
    def _get_mandatory_parameters():
        return []

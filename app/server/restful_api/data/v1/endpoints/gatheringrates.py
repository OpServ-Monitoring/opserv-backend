from .__general_data_v1 import GeneralEndpointDataV1


class GatheringRatesEndpoint(GeneralEndpointDataV1):
    @classmethod
    def _get_parent(cls):
        from ...data_api_versions_endpoint import DataApiVersionsEndpoint

        return DataApiVersionsEndpoint

    @classmethod
    def _get_children(cls) -> list:
        return []

    def _get(self) -> bool:
        from misc.constants import implemented_hardware, component_needs_arg, COMPS_TO_SYSTEM_METRICS

        values = {}

        for component_type in implemented_hardware:
            values[component_type] = {}

            if component_needs_arg(component_type):
                component_type_as_system_metric = COMPS_TO_SYSTEM_METRICS(component_type)

                for component_arg in self._outbound_gate.get_valid_arguments(component_type_as_system_metric):
                    values[component_type][component_arg] = {}
            else:
                values[component_type][None] = {}

            for component_arg in values[component_type]:
                for metric in implemented_hardware[component_type]:
                    values[component_type][component_arg][metric] = 0

        from database.unified_database_interface import UnifiedDatabaseInterface
        rdr = UnifiedDatabaseInterface.get_component_metrics_writer_reader()

        rates = rdr.get_gathering_rates()
        for tupl in rates:
            values[tupl[0]][tupl[1]][tupl[2]] = tupl[3]

        result = []
        for component_type in values:
            for component_arg in values[component_type]:
                for metric in values[component_type][component_arg]:
                    result.append({
                        "component_type": component_type,
                        "component_arg": component_arg,
                        "metric": metric,
                        "gathering_rate": values[component_type][component_arg][metric]
                    })

        self._response_holder.set_body_data({
            "values": result
        })

        return self.KEEP_PROCESSING()

    @classmethod
    def get_paths(cls):
        return [
            "/gathering-rates"
        ]

    @classmethod
    def get_name(cls):
        return "gathering rate overview"

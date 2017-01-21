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
        from misc.constants import implemented_hardware, component_needs_arg

        components = []
        for component_type in implemented_hardware:
            base_entry = {
                "component_type": component_type,
                "gathering_rate": 0
            }

            if component_needs_arg(component_type):
                for component_arg in self._outbound_gate.get_valid_arguments(component_type):
                    component = base_entry.copy()
                    component["component_arg"] = component_arg

                    components.append(component)
            else:
                components.append(base_entry)

        gathering_rates = []
        for component in components:
            component_type = component["component_type"]

            for metric in implemented_hardware[component_type]:
                gathering_rate = component.copy()
                gathering_rate["metric"] = metric

                gathering_rates.append(gathering_rate)

        self._response_holder.set_body_data({
            "values": gathering_rates
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

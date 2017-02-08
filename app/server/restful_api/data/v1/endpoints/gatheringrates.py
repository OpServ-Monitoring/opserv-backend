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
        # Collect all available component-metrics
        component_metrics_dict = self.__get_all_component_metrics()

        # Collect all saved gathering-rates
        component_metrics_dict = self.__update_component_metrics_gathering_rates(component_metrics_dict)

        # Reformat the data structure
        component_metric_list = self.__parse_component_metrics_dict_to_list(component_metrics_dict)

        self._response_holder.update_body_data({
            "values": component_metric_list
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

    @classmethod
    def __get_all_component_metrics(cls) -> dict:
        from misc.constants import implemented_hardware, component_needs_arg

        component_metrics = {}
        for component_type in implemented_hardware:
            component_metrics[component_type] = {}

            if component_needs_arg(component_type):
                for component_arg in cls._outbound_gate.get_valid_arguments(component_type):
                    component_metrics[component_type][component_arg] = {}
            else:
                component_metrics[component_type][None] = {}

            for component_arg in component_metrics[component_type]:
                for metric in implemented_hardware[component_type]:
                    component_metrics[component_type][component_arg][metric] = 0

        return component_metrics

    @classmethod
    def __update_component_metrics_gathering_rates(cls, component_metrics: dict) -> dict:
        gathering_rates = cls._outbound_gate.get_gathering_rates()
        for data_row in gathering_rates:
            component_metrics[data_row[0]][data_row[1]][data_row[2]] = data_row[3]

        return component_metrics

    @classmethod
    def __parse_component_metrics_dict_to_list(cls, component_metric_dict: dict) -> list:
        component_metric_list = []

        for component_type in component_metric_dict:
            for component_arg in component_metric_dict[component_type]:
                for metric in component_metric_dict[component_type][component_arg]:
                    component_metric_list.append({
                        "component_type": component_type,
                        "component_arg": component_arg,
                        "metric": metric,
                        "gathering_rate": component_metric_dict[component_type][component_arg][metric]
                    })

        return component_metric_list

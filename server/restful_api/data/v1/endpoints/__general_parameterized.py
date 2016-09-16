from abc import ABCMeta, abstractmethod

from server.restful_api.data.v1.endpoints.__general_data_v1 import GeneralEndpointDataV1


class GeneralEndpointParameterized(GeneralEndpointDataV1, metaclass=ABCMeta):
    def _pre_process(self):
        super(GeneralEndpointParameterized, self)._pre_process()

        mandatory_parameters = self._get_mandatory_parameters()
        if mandatory_parameters is not None:
            for parameter in mandatory_parameters:
                if not parameter["name"] in self._request_holder.get_params():
                    print("benötiger parameter nicht vorhanden")

                param_value = self._request_holder.get_params()[parameter["name"]]
                if parameter["fn"] is not None and callable(parameter["fn"]) and not parameter["fn"](param_value):
                    print("parameter erfüllt nicht anforderungen")

    @staticmethod
    @abstractmethod
    def _get_mandatory_parameters():
        pass

    @staticmethod
    def _build_parameter(name, validation_function=None):
        return {
            "name": name,
            "fn": validation_function
        }

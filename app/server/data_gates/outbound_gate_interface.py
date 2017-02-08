from abc import ABCMeta, abstractmethod


# TODO Documentation needed


class OutboundGateInterface(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def get_valid_arguments(cls, component_type: str) -> list:
        """
        Retrieves all valid arguments to the given component
        :param component_type: A string ???
        :return: An array holding all valid arguments as strings
        """

    @classmethod
    @abstractmethod
    def is_argument_valid(cls, component_type: str, component_arg: str) -> bool:
        """
        Checks whether the given argument is valid to the given component
        :param component_type: A string ???
        :param component_arg: A string ???
        :return: A boolean indicating whether the argument is valid or not
        """

    @classmethod
    @abstractmethod
    def get_measurements(cls,
                         component_type: str,
                         component_arg: str,
                         metric: str,
                         start_time: int,
                         end_time: int,
                         limit: int) -> list:
        """
        ???
        :param component_type: A String ???
        :param component_arg: A string ???, default is None
        :param metric: A string ???
        :param start_time:
        :param end_time:
        :param limit:
        :return: A string representation ??? or None
        """

    @classmethod
    @abstractmethod
    def get_last_measurement(cls, component_type: str, component_arg: str, metric: str) -> dict:
        """
        ???
        :param component_type: A String ???
        :param component_arg: A string ???, default is None
        :param metric: A string ???
        :return: A string representation ??? or None
        """

    @classmethod
    @abstractmethod
    def get_gathering_rate(cls, component_type: str, component_arg: str, metric: str) -> int:
        """
        Retrieves the currently set gathering rate in milliseconds or 0 if gathering is disabled
        :param component_type: A String ???
        :param component_arg: A string ???, default is None
        :param metric: A string ???
        :return: A integer representing the gathering rate in milliseconds in which 0 disables the gathering
        """

    @classmethod
    @abstractmethod
    def get_gathering_rates(cls) -> list:
        """
        Retrieves all gathering-rates currently persisted in the database
        :return: A list containing all gathering-rate database entries
        """

    @classmethod
    @abstractmethod
    def set_gathering_rate(cls, component_type: str, component_arg: str, metric: str, gathering_rate: int) -> None:
        """
        Sets the gathering rate of the defined component metric
        :param component_type: A string ???
        :param component_arg: A string ???
        :param metric: A string ???
        :param gathering_rate: A integer ???
        :return: None
        """

    @classmethod
    @abstractmethod
    def delete_gathering_rate(cls, component_type: str, component_arg: str, metric: str) -> None:
        """
        Sets the gathering rate of the defined component metric
        :param component_type: A string ???
        :param component_arg: A string ???, default is None
        :param metric: A string ???
        :return: None
        """

    @classmethod
    @abstractmethod
    def get_user_preference(cls, key: str) -> str:
        """
        ???
        :param key: ???
        :return: ???
        """

    @classmethod
    @abstractmethod
    def get_user_preferences(cls) -> list:
        """
        ???
        :return: ???
        """

    @classmethod
    @abstractmethod
    def set_user_preference(cls, key: str, value: str) -> None:
        """
        ???
        :param key: ???
        :param value: ???
        :return: ???
        """

    @classmethod
    @abstractmethod
    def delete_user_preference(cls, key: str) -> None:
        """
        ???
        :param key: ???
        :return: ???
        """

from abc import ABCMeta, abstractmethod

from collections import Iterable

import time

# TODO Documentation needed


class OutboundGateInterface(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def get_valid_arguments(cls, component: str) -> Iterable:
        """
        Retrieves all valid arguments to the given component
        :param component: A string ???
        :return: An array holding all valid arguments as strings
        """

    @classmethod
    @abstractmethod
    def is_argument_valid(cls, argument: str, component: str) -> bool:
        """
        Checks whether the given argument is valid to the given component
        :param argument: A string ???
        :param component: A string ???
        :return: A boolean indicating whether the argument is valid or not
        """

    @classmethod
    @abstractmethod
    def get_measurements(cls,
                         component: str,
                         metric: str,
                         argument: str=None,
                         start_time: int=0,
                         end_time: int=time.time() * 1000,
                         limit: int=5000) -> Iterable:
        """
        ???
        :param component: A String ???
        :param metric: A string ???
        :param argument: A string ???, default is None
        :param start_time:
        :param end_time:
        :param limit:
        :return: A string representation ??? or None
        """

    @classmethod
    @abstractmethod
    def get_last_measurement(cls, component: str, metric: str, argument: str=None) -> dict:
        """
        ???
        :param component: A String ???
        :param metric: A string ???
        :param argument: A string ???, default is None
        :return: A string representation ??? or None
        """

    @classmethod
    @abstractmethod
    def get_gathering_rate(cls, component: str, metric: str, argument: str=None) -> int:
        """
        Retrieves the currently set gathering rate in milliseconds or 0 if gathering is disabled
        :param component: A String ???
        :param metric: A string ???
        :param argument: A string ???, default is None
        :return: A integer representing the gathering rate in milliseconds in which 0 disables the gathering
        """

    @classmethod
    @abstractmethod
    def set_gathering_rate(cls, component: str, metric: str, gathering_rate: int, argument: str=None) -> None:
        """
        Sets the gathering rate of the defined component metric
        :param component: A string ???
        :param metric: A string ???
        :param gathering_rate: A integer ???
        :param argument: A string ???, default is None
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
    def set_user_preference(cls, key: str, value: str) -> None:
        """
        ???
        :param key: ???
        :param value: ???
        :return: ???
        """
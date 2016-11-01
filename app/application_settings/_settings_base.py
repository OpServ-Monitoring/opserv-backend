from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser, Namespace

settings = {}


class SettingsBase(metaclass=ABCMeta):
    """
    Extend this class to add further runtime settings.
    Make sure to integrate the newly created class into ???.py
    """

    @classmethod
    @abstractmethod
    def add_settings_arguments(cls, parser: ArgumentParser) -> None:
        """
        Use this function to add further arguments onto runtime arguments parser

        :param parser: an argparse.ArgumentParser object to which the args should be added
        :return: None
        """

    @classmethod
    @abstractmethod
    def validate_settings_arguments(cls, parser: ArgumentParser, args: Namespace) -> None:
        """
        Use this function to further validate the arguments added via  add_settings_arguments()  in cases in which the
        integrated validation mechanism do not fulfill your needs, e.g. when two arguments depend on each other

        :param parser: the original argparse.ArgumentParser object which parsed the arguments from standard input
        :param args: the arguments parsed by the argparse.ArgumentParser in form of a args.Namespace object
        :return: None
        """

    @classmethod
    def get_setting(cls, key):
        if key in settings:
            return settings[key]

        return None

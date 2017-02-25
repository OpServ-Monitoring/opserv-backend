import abc


class ApiManagement(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def _get_api_prefix(cls) -> str:
        """
        Give me a description
        :return:
        """

    @classmethod
    @abc.abstractmethod
    def _get_handlers(cls) -> list:
        """
        Give me a description
        :return:
        """

    @classmethod
    def get_handlers(cls) -> list:
        """
        Give me a description
        :return:
        """
        api_prefix = cls._get_api_prefix()
        raw_handlers = cls._get_handlers()

        prefix = "/apis"
        if api_prefix is not None:
            prefix += api_prefix

        return cls.add_prefix_to_handlers(prefix, raw_handlers)

    @classmethod
    def add_prefix_to_handlers(cls, prefix: str, handlers: list) -> list:
        return list(
            map(
                lambda raw_handler: cls.add_prefix_to_handler(prefix, raw_handler),
                handlers
            )
        )

    @classmethod
    def add_prefix_to_handler(cls, prefix: str, handler: tuple) -> tuple:
        if prefix is not None:
            return prefix + handler[0], handler[1]
        return handler[0], handler[1]

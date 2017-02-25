import json

import tornado.websocket
import tornado.escape


class WebsocketHandler(tornado.websocket.WebSocketHandler):
    _connections = set()

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        self.__subscriptions = set()

    def data_received(self, chunk):
        pass

    def check_origin(self, origin):
        return True

    def open(self):
        self._connections.add(self)

        # TODO Log new connection

    def on_message(self, message):
        parsed_message = tornado.escape.json_decode(message)  # TODO may raise decodeerror

        event_name = parsed_message[0]
        data = parsed_message[1]

        if event_name == "subscribe":
            self.__subscribe(
                data["component_type"],
                data["component_arg"],
                data["metric"]
            )
            # TODO Log subscriped to..    
        elif event_name == "unsubscribe":
            self.__unsubscribe(
                data["component_type"],
                data["component_arg"],
                data["metric"]
            )
            # TODO Log unsubscriped from..    

    def on_close(self):
        self._connections.remove(self)

        # TODO Log connection closed

    def __subscribe(self, component_type: str, component_arg: str, metric: str):
        self.__subscriptions.add(
            (component_type, component_arg, metric)
        )

    def __unsubscribe(self, component_type: str, component_arg: str, metric: str):
        self.__subscriptions.remove(
            (component_type, component_arg, metric)
        )

    def __is_subscribed(self, component_type: str, component_arg: str, metric: str):
        return (component_type, component_arg, metric) in self.__subscriptions

    def __on_measurement_received(self, component_type: str, component_arg: str, metric: str, timestamp: int,
                                  value: str):
        if self.__is_subscribed(component_type, component_arg, metric):
            new_measurement = [
                "new_measurement",
                {
                    "component_type": component_type,
                    "component_arg": component_arg,
                    "metric": metric,
                    "timestamp": timestamp,
                    "value": value
                }
            ]

            self.write_message(tornado.escape.json_encode(new_measurement))

    @classmethod
    def broadcast_new_measurement(cls, component_type: str, component_arg: str, metric: str, timestamp: int,
                                  value: str):
        for connection in set(cls._connections):
            if not connection.ws_connection or not connection.ws_connection.stream.socket:
                # TODO Log connection closed but not removed

                cls._connections.remove(connection)
            else:
                connection.__on_measurement_received(component_type, component_arg, metric, timestamp, value)

    """
    TO CLIENT:
    [
        "new_measurement",
        {
            "component_type" : "",
            "component_arg" : "",
            "metric" : "",
            "timestamp": 12341251,
            "value": ""
        }
    ]


    FROM CLIENT:
    [
        "subscribe",
        {
            "component_type" : "",
            "component_arg" : "",
            "metric" : ""
        }
    ]

    [
        "unsubscribe",
        {
            "component_type" : "",
            "component_arg" : "",
            "metric" : ""
        }
    ]
    """

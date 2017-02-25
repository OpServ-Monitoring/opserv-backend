import logging

import tornado.ioloop
import tornado.web
import tornado.httpserver

from application_settings.server_settings import ServerSettings
from server.apis.auth.auth_api_management import AuthApiManagement
from server.apis.docs.doc_redirects_management import DocumentationRedirectsManagement
from server.apis.rest.rest_api_management import RestApiManagement
from server.apis.websocket.websocket_api_management import WebsocketApiManagement
from server.apis.websocket.websocket_handler import WebsocketHandler
from server.static_hosting.static_hosting_management import StaticHostingManagement

log = logging.getLogger("opserv." + __name__)


class ServerManagement:
    __tornado_loop = None

    @classmethod
    def start_server(cls):
        port = cls.__get_port()
        log.debug("Starting server on port {0}".format(port))

        tls_options = cls.__get_tls_options()
        log.debug("All connections will{0}be encrypted".format(
            " NOT " if tls_options is None else " "
        ))

        tornado_server = tornado.httpserver.HTTPServer(
            cls.__get_tornado_application(),
            ssl_options=tls_options
        )
        tornado_server.listen(port)

        cls.__tornado_loop = tornado.ioloop.IOLoop.current()
        cls.__tornado_loop.start()

    @classmethod
    def stop_server(cls):
        if cls.__tornado_loop is not None:
            cls.__tornado_loop.stop()
        else:
            log.error("Tried to stop non-existing server")

    @classmethod
    def __get_port(cls):
        port = ServerSettings.get_setting(ServerSettings.KEY_PORT)

        if port is None:
            port = 8888

        return port

    @classmethod
    def __get_tls_options(cls):
        if False:  # TODO Read certificate based on runtime argument
            return {
                "certfile": "/var/pyTest/keys/ca.csr",
                "keyfile": "/var/pyTest/keys/ca.key"
            }

        return None

    @classmethod
    def __get_tornado_application(cls):
        settings = {
            "compress_response": True,
        }

        return tornado.web.Application(
            cls.__get_request_handlers(),
            **settings
        )

    @classmethod
    def __get_request_handlers(cls):
        return AuthApiManagement.get_handlers() \
               + WebsocketApiManagement.get_handlers() \
               + RestApiManagement.get_handlers() \
               + DocumentationRedirectsManagement.get_handlers() \
               + StaticHostingManagement.get_handlers()

    @classmethod
    def broadcast_new_measurement(cls, component_type: str, component_arg: str, metric: str, timestamp: int, value: str):
        if cls.__tornado_loop is not None:
            cls.__tornado_loop.add_callback(
                WebsocketHandler.broadcast_new_measurement,
                component_type, component_arg, metric, timestamp, value
            )
        else:
            log.error("Tried to broadcast a new measurement but the server does not exist (yet)")

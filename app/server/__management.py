from flask import Flask
from flask import redirect
from flask.ext.basicauth import BasicAuth
from flask_compress import Compress

import server.restful_api.flask_restful_wrapper as rest_api
import server.static_hosting.__management as static_hosting
from application_settings.server_settings import ServerSettings
from application_settings.app_settings import AppSettings
import logging

log = logging.getLogger("opserv." + __name__)


# Optional: Exchange Flask with Tornado (to add web socket support)
def start():
    """
        Starts the web server on the main thread including both the restful-api as well as the static file hosting.
    """
    log.debug("Initializing the web server")

    app = Flask(__name__, static_url_path="", static_folder="static_hosting/public/")

    rest_api.init_rest_api(app)
    static_hosting.init_static_hosting(app)

    __init_api_ref_redirect(app)

    # Support for CORS-request even for static hosting
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    Compress(app)

    # TODO Future version: Re-enable TLS context = ('server/ssl.cert', 'server/ssl.key')

    port = ServerSettings.get_setting(ServerSettings.KEY_PORT)
    if port is None:
        port = 31337

    password = AppSettings.get_setting(AppSettings.KEY_PASSWORD)
    if password is not None:
        app.config['BASIC_AUTH_USERNAME'] = 'opserv'
        app.config['BASIC_AUTH_PASSWORD'] = password
        app.config['BASIC_AUTH_FORCE'] = True

        basic_auth = BasicAuth(app)

    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)
    # to do: Generate certificate

    # This point shouldn't be reached
    log.error("An error occurred. Web server shutting down!")


def __init_api_ref_redirect(app):
    @app.route('/apiref', defaults={'path': ''})
    @app.route('/apiref/<path:path>')
    def catch_all(path):
        base_api_doc_url = "https://opserv-monitoring.github.io/opserv-backend/docs/apis/restful"

        import re
        pattern = "(^data/(v1|current)/(cpus|disks|gpus|partitions|processes|networks|cpu-cores))(/[^/]+)((/[^/]+)*)"
        search_result = re.search(pattern, path)

        if search_result is None:
            pattern = "(^preferences/(v1|current))(/[^/]+)"
            search_result = re.search(pattern, path)

            if search_result is None:
                parsed_path = path
            else:
                parsed_path = search_result.group(2) + "/id"
        else:
            parsed_path = search_result.group(1) + "/id" + search_result.group(5)

        if len(parsed_path) > 0:
            parsed_path = "/" + parsed_path

        redirect_url = base_api_doc_url + parsed_path

        return redirect(redirect_url, code=302)

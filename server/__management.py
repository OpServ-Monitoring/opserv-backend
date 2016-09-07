from flask import Flask

import server.restful_api.__management as rest_api
import server.static_hosting.__management as static_hosting


def start():
    """
        Starts the web server on the main thread including both the restful-api as well as the static file hosting.
    """
    print("Initializing the web server")

    app = Flask(__name__, static_url_path="", static_folder="static_hosting/public/")

    rest_api.init_rest_api(app)
    static_hosting.init_static_hosting(app)

    app.run(host='127.0.0.1', port=31337, debug=False, threaded=False)
    # TODO Make the port configurable
    # TODO add SSL Context for HTTPS usage   ssl_context=context

    # This point shouldn't be reached
    print("An error occurred. Web server shutting down!")

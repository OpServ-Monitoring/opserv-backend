from flask import Flask

import server.restful_api.flask_restful_wrapper as rest_api
import server.static_hosting.__management as static_hosting


def start():
    """
        Starts the web server on the main thread including both the restful-api as well as the static file hosting.
    """
    print("Initializing the web server")

    app = Flask(__name__, static_url_path="", static_folder="static_hosting/public/")

    rest_api.init_rest_api(app)
    static_hosting.init_static_hosting(app)

    # Support for CORS-request even for static hosting
    # TODO full CORS-support should be removed in a future version
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    app.run(host='127.0.0.1', port=31337, debug=False, threaded=True)
    # TODO Make the port configurable
    # TODO add SSL Context for HTTPS usage   ssl_context=context

    # This point shouldn't be reached
    print("An error occurred. Web server shutting down!")

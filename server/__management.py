from flask import Flask
from flask_compress import Compress

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
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    Compress(app)

    context = ('server/ssl.cert', 'server/ssl.key')

    app.run(host='127.0.0.1', port=31337, ssl_context=context, debug=False, threaded=True)
    # to do: Make the port configurable
    # to do: Generate certificate

    # This point shouldn't be reached
    print("An error occurred. Web server shutting down!")

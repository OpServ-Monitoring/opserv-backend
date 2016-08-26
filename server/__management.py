import server.restful_api.__management as rest_api
import server.static_hosting.__management as static_hosting


from flask import Flask


def start():
    print("Initializing the web server")

    app = Flask(__name__, static_url_path="", static_folder="static_hosting/public/")

    rest_api.init_rest_api(app)
    static_hosting.init_static_hosting(app)

    app.run(host='127.0.0.1', port=31337, debug=False, threaded=True)
    # , ssl_context=context)

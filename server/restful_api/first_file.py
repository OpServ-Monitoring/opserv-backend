from flask import Flask


def try_me():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Flask is running!'

    app.run()

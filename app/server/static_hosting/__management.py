from flask import send_from_directory


def init_static_hosting(app):
    @app.route('/')
    def send_index():
        return send_from_directory(directory='static_hosting/public/', filename='index.html')

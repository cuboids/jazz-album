import os
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for the Flask app

    with app.app_context():
        from . import main
        app.register_blueprint(main.bp)

    return app

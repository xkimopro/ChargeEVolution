from flask import Flask , request, abort
import sys
import os


sys.path.append(os.path.dirname(__file__))

from custom_routes.users import users
from custom_routes.admin import admin
from custom_routes.sessions import sessions
from custom_routes.stations import stations




def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    # Blueprints/Routes
    app.register_blueprint(users, url_prefix='/api/users')
    app.register_blueprint(admin, url_prefix='/api/admin')
    app.register_blueprint(sessions, url_prefix='/api/sessions')
    app.register_blueprint(stations, url_prefix='/api/stations')


    @app.route('/api')
    def index():
        return "<h1>Welcome to EVolution-Charge Web Services<h1>"

    

    return app
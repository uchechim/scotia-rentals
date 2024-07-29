#this file is used to define how the flask application is created.

from flask import Flask
from flask_cors import CORS
from flask_app.routes.auth import auth_blueprint
from flask_app.routes.listings import listings_blueprint
from flask_app.routes.favorites import favorites_blueprint
from flask_app.routes.payments import payments_blueprint
from config import Config

def create_app():
    application = Flask(__name__)
    CORS(application)

    application.config.from_object(Config) #set the application's config to use the defined configuration in config.py
    
    #register api blueprints - this makes the application modular.
    #this way, as the application grows, I can easily separate the application's logic on the Flask Level
    application.register_blueprint(auth_blueprint)
    application.register_blueprint(listings_blueprint)
    application.register_blueprint(favorites_blueprint)
    application.register_blueprint(payments_blueprint)

    return application
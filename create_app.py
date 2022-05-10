""" Create app """

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from exts import db
import os
from models import Exchange, Account
from route_exchanges import exchange_api
from route_accounts import account_api
from flask_cors import CORS

def create_app():
    # Create a Flask instance
    app = Flask(__name__)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/exchange'
    
    # Flask configuration
    pjdir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(pjdir, "data.sqlite")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "HS256"
    
    # Cross origin resource sharing
    CORS(app)
    
    db.init_app(app) # Connect app to database
    # db.create_all()  # Create database
    
    # JWT authentication manager
    JWTManager(app)

    # Set API
    api=Api(app, doc='/docs')
    api.add_namespace(exchange_api)
    api.add_namespace(account_api)

    """ This is a test """
    from flask_restx import Resource, Namespace
    test_api=Namespace('test')
    api.add_namespace(test_api)
    @test_api.route("/")
    class TestResource(Resource):
        def get(self):
            return "Hello Flask!"
         
    return app
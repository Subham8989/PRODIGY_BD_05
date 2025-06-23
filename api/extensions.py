from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

db = SQLAlchemy()
api = Api()
jwt = JWTManager()
migrate = Migrate()

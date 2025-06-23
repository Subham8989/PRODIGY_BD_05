from flask import Flask

from api.auth.login import Login
from .extensions import db, api, jwt
from .config import Config
from .extensions import migrate

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)

  from api.auth.register import Register
  api.add_resource(Register, "/auth/register")
  api.add_resource(Login, "/auth/login")

  api.init_app(app)
  jwt.init_app(app)
  migrate.init_app(app, db, directory="api/migrations")
  
  return app
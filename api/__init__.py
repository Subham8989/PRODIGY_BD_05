from flask import Flask

from .extensions import db, api, jwt
from .config import Config
from .extensions import migrate

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)
  jwt.init_app(app)

  from api.auth.register import Register
  from api.auth.login import Login
  from api.auth.logout import Logout
  from .routes import RoomList, RoomFirst, BookingsList, Bookings

  api.add_resource(Register, "/auth/register")
  api.add_resource(Login, "/auth/login")
  api.add_resource(Logout, "/auth/logout")
  api.add_resource(RoomList, "/rooms")
  api.add_resource(RoomFirst, "/rooms/<int:room_id>")
  api.add_resource(BookingsList, "/bookings")
  api.add_resource(Bookings, "/bookings/<string:booking_id>")

  api.init_app(app)
  migrate.init_app(app, db, directory="api/migrations")
  
  return app
from flask_restful import reqparse, Resource
from flask_bcrypt import check_password_hash
from flask_jwt_extended import (
  create_access_token,
  create_refresh_token,
  set_access_cookies,
  set_refresh_cookies
)
from flask import make_response
from ..models import User
from ..extensions import db

parser = reqparse.RequestParser()
parser.add_argument("username", type=str, required=True, help="Username must be provided!")
parser.add_argument("password", type=str, required=True, help="Password must be provided!")

class Login(Resource):
  def post(self):
    args = parser.parse_args()
    username = args["username"]
    password = args["password"]

    user = db.session.execute(db.select(User).filter_by(username=username)).first()
    if not user:
      return { "message": "User not found" }, 404
    
    if check_password_hash(user[0].password, password):
      access_token = create_access_token(identity=username)
      refresh_token = create_refresh_token(identity=username)
      response = make_response({ "message": "Login successful!" }, 200)
      set_access_cookies(response, access_token)
      set_refresh_cookies(response, refresh_token)
      return response
    
    return { "message": "Wrong Password!" }, 401
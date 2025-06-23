from flask_restful import Resource
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from flask import make_response

class Logout(Resource):
  @jwt_required()
  def post(self):
    response = make_response({ "message": "Successfully logged out!" }, 202)
    unset_jwt_cookies(response)
    return response
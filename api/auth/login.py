from flask_restful import reqparse, Resource
from flask_bcrypt import check_password_hash
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
      return { "message": "Login successful!" }, 200
    
    return { "message": "Wrong Password!" }, 401
from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash
from sqlalchemy.exc import IntegrityError

from ..utils import emailtype
from ..models import User
from ..extensions import db

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="Name must be provided!", required=True)
parser.add_argument("username", type=str, help="Username must be provided!", required=True)
parser.add_argument("password", type=str, help="Password must be provided!", required=True)
parser.add_argument("email", type=emailtype, help="Email must be valid!", required=True)
parser.add_argument("age", type=int, help="Age must be an Integer!", required=True)

class Register(Resource):
  def post(self):
    args = parser.parse_args()
    name = args["name"]
    username = args["username"]
    user = db.session.execute(db.select(User).filter_by(username=username)).first()
    if user:
      return { "message": "User already exists" }, 409
    password = generate_password_hash(args["password"])
    email = args["email"]
    age = args["age"]

    try:
      user = User(
        name=name,
        username=username,
        password=password,
        email=email,
        age=age
      )

      db.session.add(user)
      db.session.commit()
    except IntegrityError:
      db.session.rollback()
      return { "message": "Database constraint violated" }, 409
    except Exception as e:
      db.session.rollback()
      return { "message": f"Unexpected server error => {e}" }, 500
    
    return { "id": user.id, "message": "User created" }, 201
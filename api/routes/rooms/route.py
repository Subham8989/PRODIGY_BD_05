from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from ...extensions import db
from ...models import Room
from sqlalchemy.exc import IntegrityError

parser = reqparse.RequestParser()
parser.add_argument("id", type=int, required=True, help="Room ID must be valid!")
parser.add_argument("price", type=int, required=True, help="Price must be valid!")

put_parser = reqparse.RequestParser()
put_parser.add_argument("price", type=int, required=True, help="Price must be valid!")

class RoomList(Resource):
  @jwt_required()
  def get(self):
    rooms = db.session.execute(db.select(Room))
    print(rooms)
    roomlist = list()
    for room in rooms:
      data = {
        "id": room[0].id,
        "price": room[0].price,
        "owner_id": room[0].owner_id
      }
      roomlist.append(data)
      
    return roomlist, 200
  
  @jwt_required()
  def post(self):
    args = parser.parse_args()
    id = args["id"]
    price = args["price"]
    room = db.session.execute(db.select(Room).filter_by(id=id)).first()
    if room:
      return { "message": "Room already exists!" }, 409
    
    try:
      new_room = Room(
        id=id,
        price=price,
        owner_id=None
      )
      db.session.add(new_room)
      db.session.commit()
    except IntegrityError:
      db.session.rollback()
      return { "message": "Database constaint violated" }, 409
    except Exception as e:
      db.session.rollback()
      return { "message": f"Unexpected server error => {e}" }, 500
    
    return { "message": "Room created" }, 201
  

class RoomFirst(Resource):
  @jwt_required()
  def get(self, room_id):
    room = db.session.execute(db.select(Room).filter_by(id=room_id)).first()
    if not room:
      return { "message": "Room not found!" }, 404
    
    return { "id": room[0].id, "price": room[0].price, "owner_id": room[0].owner_id }
  
  @jwt_required()
  def put(self, room_id):
    args = put_parser.parse_args()
    room = db.session.execute(db.select(Room).filter_by(id=room_id)).first()
    if not room:
      return { "message": "Room not found!" }, 404
    
    try:
      room[0].price = args["price"]
      db.session.commit()
    except IntegrityError:
      db.session.rollback()
      return { "message": "Database constraints violated" }, 409
    except Exception as e:
      db.session.rollback()
      return { "message": f"Server error occured => {e}" }, 500
    
    return { "message": "Room data changed" }, 200
  
  @jwt_required()
  def delete(self, room_id):
    room = db.session.execute(db.select(Room).filter_by(id=room_id)).scalars().first()
    if not room:
      return { "message": "Room not found" }, 404
    
    try:
      db.session.delete(room)
      db.session.commit()
    except Exception as e:
      return { "message": f"Server error occured => {e}" }, 500
    
    return { "message": "Room deleted successfully" }, 202

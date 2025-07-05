from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from ...models import Booking
from ...extensions import db
from ...utils import datetype

parser = reqparse.RequestParser()
parser.add_argument("user_id", type=str, required=True, help="User ID must be given!")
parser.add_argument("room_id", type=str, required=True, help="Room ID must be given!")
parser.add_argument("check_in", type=datetype, required=True, help="Check in date must be in YYYY-MM-DD Format!")
parser.add_argument("check_out", type=datetype, required=True, help="Check out date must be in YYYY-MM-DD Format!")

class BookingsList(Resource):
  @jwt_required()
  def get(self):
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")

    query = db.select(Booking)

    if check_in:
      try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        query = query.where(Booking.check_in >= check_in_date)
      except ValueError:
        return { "message": "Invalid check_in format. Use YYYY-MM-DD." }, 400

    if check_out:
      try:
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        query = query.where(Booking.check_out <= check_out_date)
      except ValueError:
        return { "message": "Invalid check_out format. Use YYYY-MM-DD." }, 400

    bookings = db.session.execute(query).scalars().all()

    booking_list = [
      {
        "id": b.id,
        "user_id": b.user_id,
        "room_id": b.room_id,
        "check_in": str(b.check_in),
        "check_out": str(b.check_out)
      }
      for b in bookings
    ]

    return booking_list, 200

  @jwt_required()
  def post(self):
    args = parser.parse_args()
    check_in = datetime.strptime(args["check_in"], "%Y-%m-%d")
    check_out = datetime.strptime(args["check_out"], "%Y-%m-%d")
    if check_out < check_in:
      return { "message": "Check out date must be later than check in date!" }, 400
    room = args["room_id"]
    bookings = db.session.execute(db.select(Booking))
    booking_list = list()
    for booking in bookings:
      booking_list.append({
        "room_id": booking[0].room_id,
        "check_in": booking[0].check_in,
        "check_out": booking[0].check_out
      })
    temp = [x for x in booking_list if ((((datetime.strptime(args["check_in"], "%Y-%m-%d") > datetime.strptime(x["check_in"], "%Y-%m-%d")) and (datetime.strptime(args["check_in"], "%Y-%m-%d") < datetime.strptime(x["check_out"], "%Y-%m-%d"))) or ((datetime.strptime(args["check_out"], "%Y-%m-%d") > datetime.strptime(x["check_in"], "%Y-%m-%d")) and (datetime.strptime(args["check_out"], "%Y-%m-%d") < datetime.strptime(x["check_out"], "%Y-%m-%d")))) and (args["room_id"] == x["room_id"]))]

    if len(temp) != 0:
      return { "message": "Timeslot already booked" }, 400

    try:
      booking = Booking(
        user_id=args["user_id"],
        room_id=args["room_id"],
        check_in=args["check_in"],
        check_out=args["check_out"]
      )

      db.session.add(booking)
      db.session.commit()
    except IntegrityError:
      return { "message": "Database constraint violated!" }, 409
    except Exception as e:
      return { "message": f"Server error occured => {e}" }, 500
    
    return { "message": f"Booking created" }, 200

class Bookings(Resource):
  @jwt_required()
  def get(self, booking_id):
    booking = db.session.execute(db.select(Booking).filter_by(id=booking_id)).first()
    if not booking:
      return { "message": "Booking not found!" }, 404
    
    return { "id": booking[0].id, "user_id": booking[0].user_id, "room_id": booking[0].room_id, "check_in": booking[0].check_in, "check_out": booking[0].check_out }, 200

  @jwt_required()
  def delete(self, booking_id):
      booking = db.session.execute(db.select(Booking).filter_by(id=booking_id)).scalars().first()
      if not booking:
          return { "message": "Booking not found!" }, 404

      db.session.delete(booking[0])
      db.session.commit()
      return { "message": "Booking deleted successfully." }, 200

  @jwt_required()
  def put(self, booking_id):
      booking = db.session.execute(db.select(Booking).filter_by(id=booking_id)).first()
      if not booking:
          return { "message": "Booking not found!" }, 404

      args = parser.parse_args()
      check_in = datetime.strptime(args["check_in"], "%Y-%m-%d")
      check_out = datetime.strptime(args["check_out"], "%Y-%m-%d")

      if check_out < check_in:
          return { "message": "Check out date must be later than check in date!" }, 400

      # Check for conflicts excluding the current booking
      existing_bookings = db.session.execute(db.select(Booking).filter(Booking.id != booking_id)).all()
      for b in existing_bookings:
          b = b[0]
          if b.room_id == args["room_id"] and not (check_out <= b.check_in or check_in >= b.check_out):
              return { "message": "Timeslot already booked" }, 400

      try:
          b = booking[0]
          b.user_id = args["user_id"]
          b.room_id = args["room_id"]
          b.check_in = args["check_in"]
          b.check_out = args["check_out"]

          db.session.commit()
      except IntegrityError:
          return { "message": "Database constraint violated!" }, 409
      except Exception as e:
          return { "message": f"Server error occurred => {e}" }, 500

      return { "message": "Booking updated successfully." }, 200

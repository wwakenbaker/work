from typing import TYPE_CHECKING
from main_app.app import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


class Client(Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    def __repr__(self):
        return f"{self.name} {self.surname}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(Model):
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, default=False)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.address} {self.id}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(Model):
    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    def __repr__(self):
        return f"{self.client_id} {self.parking_id}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

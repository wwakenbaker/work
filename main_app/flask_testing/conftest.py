import pytest

from datetime import datetime
from main_app.app import create_app, db as _db
from main_app.models import Client, Parking, ClientParking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        client = Client(
            name="name",
            surname="surname",
            credit_card="1234123412341234",
            car_number="1234567890",
        )
        parking = Parking(
            address="address", opened=True,
            count_places=10, count_available_places=10
        )
        client_parking = ClientParking(
            client_id=1, parking_id=1, time_in=datetime.now(), time_out=None
        )
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db

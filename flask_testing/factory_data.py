import factory

from module_29_testing.hw.models import Client, Parking, ClientParking
from module_29_testing.hw.app import db


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.Faker('credit_card_number')
    car_number = factory.Faker('license_plate')

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    opened = factory.Faker('boolean')
    count_places = factory.Faker('random_int', min=40, max=50)
    count_available_places = factory.Faker('random_int', min=0, max=40)

class ClientParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ClientParking
        sqlalchemy_session = db.session

    client_id = factory.SubFactory(ClientFactory)
    parking_id = factory.SubFactory(ParkingFactory)
    time_in = factory.Faker('past_date', start_date="-1d")
    time_out = factory.Faker('future_date', end_date="+1d")
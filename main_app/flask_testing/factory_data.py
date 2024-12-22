import factory
from factory import Faker, SubFactory
from main_app.models import Client, Parking, ClientParking
from main_app.app import db


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name: Faker = factory.Faker('first_name')
    surname: Faker = factory.Faker('last_name')
    credit_card: Faker = factory.Faker('credit_card_number')
    car_number: Faker = factory.Faker('license_plate')

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address: Faker = factory.Faker('address')
    opened: Faker = factory.Faker('boolean')
    count_places: Faker = factory.Faker('random_int', min=40, max=50)
    count_available_places: Faker = factory.Faker('random_int', min=0, max=40)

class ClientParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ClientParking
        sqlalchemy_session = db.session

    client_id: SubFactory = factory.SubFactory(ClientFactory)
    parking_id: SubFactory = factory.SubFactory(ParkingFactory)
    time_in: Faker = factory.Faker('past_date', start_date="-1d")
    time_out: Faker = factory.Faker('future_date', end_date="+1d")
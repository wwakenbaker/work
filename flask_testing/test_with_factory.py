from .factory_data import ClientFactory, ParkingFactory

def test_add_client(client):
    _client = ClientFactory()
    data = {"name": _client.name, "surname": _client.surname,
            "credit_card": _client.credit_card, "car_number": _client.car_number}
    rv = client.post("/clients", data=data)
    cl = client.get("/clients/2").get_json()
    assert rv.status_code == 201
    assert cl['client']['name'] == _client.name
    assert cl['client']['surname'] == _client.surname
    assert cl['client']['credit_card'] == _client.credit_card
    assert cl['client']['car_number'] == _client.car_number


def test_add_parking(client):
    _parking = ParkingFactory()
    data = {"address": _parking.address, "opened": _parking.opened,
            "count_places": _parking.count_places, "count_available_places": _parking.count_available_places}
    rv = client.post("/parkings", data=data)
    assert rv.status_code == 201
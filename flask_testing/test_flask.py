import pytest
from .conftest import _db, ClientParking, Parking

@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


def test_add_client(client):
    data = {"name": "Andrew", "surname": "Does", "credit_card": "1234212123456", "car_number": "ABas34"}
    rv = client.post("/clients", data=data)
    cl = client.get("/clients/2").get_json()
    assert rv.status_code == 201
    assert cl['client']['name'] == 'Andrew'
    assert cl['client']['surname'] == 'Does'
    assert cl['client']['credit_card'] == '1234212123456'
    assert cl['client']['car_number'] == 'ABas34'

def test_add_parking(client):
    data = {"address": "123 Main St", "opened": True, "count_places": 10, "count_available_places": 10}
    rv = client.post("/parkings", data=data)
    assert rv.status_code == 201

@pytest.mark.parking
def test_add_client_parking(client):
    data = {"client_id": 1, "parking_id": 1, "time_in": "2025-01-01 12:00:00"}  # datetime.now()
    rv = client.post("/client_parking", data=data)
    check = _db.session.query(ClientParking).filter_by(client_id=1, parking_id=1).first().id
    assert rv.status_code == 201
    assert check == 1

@pytest.mark.parking
def test_delete_client_parking(client):
    data = {"client_id": 1, "parking_id": 1}  # datetime.now()
    places_before = _db.session.query(Parking).filter_by(id=1).first().count_available_places
    rv = client.delete("/client_parking", data=data)
    places_after = _db.session.query(Parking).filter_by(id=1).first().count_available_places
    assert rv.status_code == 200
    assert places_after -1 == places_before

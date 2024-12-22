from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .models import Client, Parking, ClientParking

    with app.app_context():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route('/clients', methods=['GET'])
    def get_clients_handler():
        clients = Client.query.all()
        return {'clients': [client.to_json() for client in clients]}

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client_handler(client_id):
        client = Client.query.get_or_404(client_id)
        return {'client': client.to_json()}

    @app.route('/clients', methods=['POST'])
    def add_client_handler():
        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        credit_card = request.form.get('credit_card', type=str)
        card_number = request.form.get('car_number', type=str)
        client = Client(name=name, surname=surname, credit_card=credit_card, car_number=card_number)
        db.session.add(client)
        db.session.commit()
        return {'Клиент успешно добавлен, client_id:': client.id}, 201

    @app.route('/parkings', methods=['POST'])
    def add_parking():
        address = request.form.get('address', type=str)
        opened = request.form.get('opened', type=bool)
        count_places = request.form.get('count_places', type=int)
        parking = Parking(address=address, opened=opened, count_places=count_places, count_available_places=count_places)
        db.session.add(parking)
        db.session.commit()
        return {'Парковочная зона успешно добавлена, parking_id:': parking.id}, 201

    @app.route('/client_parking', methods=['POST'])
    def add_client_parking():
        parking_id = request.form.get('parking_id', type=int)
        client_id = request.form.get('client_id', type=int)
        if parking_id in [parking.id for parking in Parking.query.all()]:
            parking = Parking.query.get(parking_id)
            if parking.opened and parking.count_available_places > 0:
                user = ClientParking(client_id=client_id,
                                     parking_id=parking_id,
                                     time_in=datetime.now())
                db.session.add(user)
                parking.count_available_places -= 1
                db.session.commit()
                return {'Клиент успешно зарегистрирован в парковочной зоне, client_id:': user.id}, 201
            else:
                return {'error': 'Парковочная зона закрыта или полностью занята'}, 403
        else:
            return {'error': 'Парковочная зона не найдена'}, 404

    @app.route('/client_parking', methods=['DELETE'])
    def delete_client_parking():
        parking_id = request.form.get('parking_id', type=int)
        client_id = request.form.get('client_id', type=int)
        if parking_id in [parking.id for parking in Parking.query.all()]:
            parking = Parking.query.get(parking_id)
            client = Client.query.get(client_id)
            obj = ClientParking.query.filter_by(client_id=client_id, parking_id=parking_id).first()
            if obj:
                if client.credit_card:
                    obj.time_out = datetime.now()
                    db.session.delete(obj)
                    parking.count_available_places += 1
                    db.session.commit()
                    return {'Клиент успешно сдал парковочную зону, client_id:': client_id}, 200
                else:
                    return {'error': 'Клиент не имеет кредитной карты'}, 403
            else:
                return {'error': 'Связи с клиентом и парковочной зоной не найдены'}, 404
        else:
            return {'error': 'Парковочная зона не найдена'}, 404


    return app




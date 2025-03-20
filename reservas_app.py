from flask import Flask
from src.reservas.database.db import init_db
from src.reservas.blueprints import reserva_bp
from src.events import setup_rabbitmq 



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jdrt:traxi_prueba@localhost/reservas'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)
    setup_rabbitmq()

    app.register_blueprint(reserva_bp, url_prefix='/reservas')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
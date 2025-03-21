from flask import Flask
from .src.pasajeros.database.db import init_db
from .src.pasajeros.blueprints import pasajeros_bp
from .src.pasajeros.utils.events import setup_rabbitmq



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jdrt:traxi_prueba@pasajeros-db:5432/pasajeros'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)
    setup_rabbitmq()

    app.register_blueprint(pasajeros_bp, url_prefix='/pasajeros')
    return app



if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
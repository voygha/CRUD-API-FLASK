from flask import Flask
from models.item import db
from routes.items_routes import items_bp

from config import Config

app = Flask(__name__)


#Configurar la base de datos (En este caso SQLite)
app.config.from_object(Config)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Inicializar la base de datos
db.init_app(app)

#Registrar los blueprints (rutas)
app.register_blueprint(items_bp, url_prefix= '/items')


# Crear la base de datos (solo si no existe)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

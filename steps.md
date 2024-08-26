# Instalar dependencias / Install Dependencies

```bash
pip install Flask
```

```bash
pip install SQLAlchemy
```

```bash
pip install Flask-SQLAlchemy
```

# Estructura del Proyecto / Proyect Structure
```txt
my_project/
│
├── src/
│   ├── app.py
│   ├── config.py
│   ├── models/
│   │   └── item.py
│   ├── routes/
│   │   └── items.routes.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_items.py
│
├── migrations/  (opcional, si usas herramientas de migración como Flask-Migrate) (optional if you use tools of migration as Flask-Migrate)
├── venv/        (opcional, carpeta del entorno virtual) (Optional folder of virtual environment)
├── requirements.txt
└── README.md (Documentacion del proyecto) (Project Documentation) 
```

## Aclaraciones / Clarifications
- En la carpeta src el archivo `__init__.py` puedes dejarlo vacio.
- En la carpeta test, el archivo `__init__.py` puedes dejarlo vacio.
- In the folder src, the file `__init__.py` you can leave the file  `__init__.py` empty.
- In the folder test, the file `__init__.py` you can leave the file  `__init__.py` empty.


# Inicializar el Proyecto / Project initialization

En esta parte de la configuracion vamos a levantar nuestro servidor con Flask y crearemos la base de datos con SqlAlchemy si no existe.


In this part of configuration we start the server with Flask and the database with SqlAlchemy if it doesn't exist

## Archivo  `config.py` / File `config.py`

Vamos al archivo /src/config.py


Go to the file /src/config.py

Vamos a crear la instancia a la base de datos


We create the Database instance

```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

```

## Archivo `index.py` / File `index.py`
Vamos al archivo /src/index.py


Go to the file /src/index.py

### Creacion del servidor e Importaciones necesarias / Create the server and require some imports 
```python
from flask import Flask
from models.item import db
from routes.items_routes import items_bp

from config import Config

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
```

### Configurar la base de datos e inicializarla / Database configuration and initialization

```python
#Configurar la base de datos (En este caso SQLite)
app.config.from_object(Config)

#Inicializar la base de datos
db.init_app(app)
```
### Registrar las rutas /  Register of the routes
```python
#Registrar los blueprints (rutas)
app.register_blueprint(items_bp, url_prefix= '/items')
```

El archivo `index.py` completo quedaria asi:


The complete `index.py` file would look like this:

```python
from flask import Flask
from models.item import db
from routes.items_routes import items_bp

from config import Config

app = Flask(__name__)

#Configurar la base de datos (En este caso SQLite)
app.config.from_object(Config)

#Inicializar la base de datos
db.init_app(app)

#Registrar los blueprints (rutas)
app.register_blueprint(items_bp, url_prefix= '/items')

# Crear la base de datos (solo si no existe)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

```

## Archivo `item.py` / File `item.py`

Vamos al archivo /src/models/items.py

Go to the file /src/models/items.py

```python
#importamos SqlAlchemy - import SqlAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Creamos nuestro modelo de datos - We create items model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
```

Con la base de datos creada, podemos comenzar a crear las rutas de nuestra API para manipular la informacion de la base de datos


With the database created, we can begin to create our API routes to manipulate the database information.


## Archivo `items_routes.py` / File `items_routes.py`
Vamos al archivo /src/routes/items_routes.py

Go to the file /src/routes/items_routes.py

En este archivo vamos a construir nuestra API con operaciones CRUD

In this file we build our CRUD operations

Primero vamos a importar los paquetes necesarios

Firts, we import the necesary package 


```python
from sqlalchemy.orm import Session

from flask import Blueprint, request, jsonify

from models.item import db, Item

items_bp = Blueprint('items', __name__)
```

### Ruta para crear nuevo item / Route to create a new item

```python
from sqlalchemy.orm import Session
from flask import Blueprint, request, jsonify
from models.item import db, Item

items_bp = Blueprint('items', __name__)

#Ruta para crear un nuevo item - Create a new item
@items_bp.route('/', methods=['POST'])
def create_item():
    data = request.get_json()
    #obtener los datos del request - get all data of the request 
    new_item = Item(name= data['name'], description= data.get('description'))
    #operacion para insertar el item en la bd - operation to insert a new item in the database
    db.session.add(new_item)
    #guardar la insercion en la bd - save the item in the database
    db.session.commit()
    return jsonify({ "message": "Item Created", "item": { "id": new_item.id, "name": new_item.name, "description": new_item.description}}), 201
```

### Ruta para obtener todos los items / Route to get all items
```python
from sqlalchemy.orm import Session
from flask import Blueprint, request, jsonify
from models.item import db, Item

items_bp = Blueprint('items', __name__)

# Ruta para obtener todos los items
@items_bp.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    #devuelve un objeto con todos los items encontrados
    #return an object with all  items
    result = [{"id": item.id, "name": item.name, "description": item.description } for item in items]
    return jsonify(result)
```

### Ruta para obtener Item por ID / Route to get Item by ID
```python
from sqlalchemy.orm import Session
from flask import Blueprint, request, jsonify
from models.item import db, Item

items_bp = Blueprint('items', __name__)

#Ruta para obtener un item por Id
@items_bp.route('/<item_id>', methods=['GET'])
def get_item(item_id):
    # Si el parametro que recibe no es numerico
    # if the parameter is not numeric
    if not item_id.isdigit():
        return jsonify({ "error": "La ruta espera un id numerico" }), 400
    
    # Acceder a la sesión actual
    # Access the current database session
    session = db.session
    
    #Obtiene el Item
    #Get the item by ID
    # Usar Session.get() en lugar de Query.get()
    item = session.get(Item, item_id)
    #Si no existe el Item
    # if ID doesn't exist
    if item is None:
        return jsonify({ "error": "El Item con el Id proporcionado no existe ".format(item_id)}), 404
    
    # Si el Id coincide con un item existente => retorna los datos del item
    #If item ID exist
    return jsonify({ "id": item.id, "name": item.name, "description": item.description })
```


### Ruta para actualizar un item / Route to update an item
```python
from sqlalchemy.orm import Session
from flask import Blueprint, request, jsonify
from models.item import db, Item

items_bp = Blueprint('items', __name__)

# Ruta para actualizar un item
@items_bp.route('/<item_id>', methods=['PUT'])
def update_item(item_id):
    if not item_id.isdigit():  # Verifica si item_id es numérico # Verify if Item ID is a number
        return jsonify({"error": "The route expects a numeric ID."}), 400
    
    # Acceder a la sesión actual
    # Access the current database session
    session = db.session
    
    # Usar Session.get() en lugar de Query.get()
    item = session.get(Item, item_id)
    #si el id del item no existe
    #If item ID doesn't exist
    if item is None:
        return jsonify({"error": "Item with ID  does not exist. Please try another ID.".format(item_id)}), 404
    
    #Si existe el Id
    #If the item ID exist
    data = request.get_json()
    item.name = data['name']
    item.description = data.get('description')
    #Guarda los datos actualizados
    #Save changes
    db.session.commit()
    return jsonify({"message": "Item updated", "item": {"id": item.id, "name": item.name, "description": item.description}})
```

### Ruta para eliminar un item / Route to delete an item

```python
from sqlalchemy.orm import Session
from flask import Blueprint, request, jsonify
from models.item import db, Item

items_bp = Blueprint('items', __name__)

#Ruta para eliminar un Item
@items_bp.route('/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    # Si el id no es un numero
    #if the item ID is not a number
    if not item_id.isdigit():
        return jsonify({ "error": "La ruta espera un Id numerico" }), 400
    
    # Acceder a la sesión actual
    # Access the current database session
    session = db.session

    #Busca el item por el id
    #Search the item by ID
    # Usar Session.get() en lugar de Query.get()
    item = session.get(Item, item_id)
    
    # Si no existe el Item
    # If the item ID doesn't exist
    if item is None:
        return jsonify({"error": "El Item con el id proporcionado no existe".format(item_id)}), 404
    
    #Si el item existe
    #If the item exist
    db.session.delete(item)
    #Elimina el item de la base de datos
    #Delete the item to the database
    db.session.commit()
    # Retorna el mensaje de que se borro el item
    # Retorna los datos del item eliminado
    return jsonify({ "message": "Item deleted", "item": { "id": item.id, "name": item.name, "description": item.description} })
```
## Archivo `items_routes.py` Completo / File `items_routes.py` Completed

```python
from sqlalchemy.orm import Session

from flask import Blueprint, request, jsonify

from models.item import db, Item

items_bp = Blueprint('items', __name__)

#Ruta para crear un nuevo item
@items_bp.route('/', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name= data['name'], description= data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({ "message": "Item Created", "item": { "id": new_item.id, "name": new_item.name, "description": new_item.description}}), 201

# Ruta para obtener todos los items
@items_bp.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    result = [{"id": item.id, "name": item.name, "description": item.description } for item in items]
    return jsonify(result)

#Ruta para obtener un item por Id
@items_bp.route('/<item_id>', methods=['GET'])
def get_item(item_id):
    # Si el parametro que recibe no es numerico
    if not item_id.isdigit():
        return jsonify({ "error": "La ruta espera un id numerico" }), 400
    
    # Acceder a la sesión actual
    session = db.session
    
    #Obtiene el Item
    # Usar Session.get() en lugar de Query.get()
    item = session.get(Item, item_id)
    #Si no existe el Item
    if item is None:
        return jsonify({ "error": "El Item con el Id proporcionado no existe ".format(item_id)}), 404
    # Si el Id coincide con un item existente => retorna los datos del item
    return jsonify({ "id": item.id, "name": item.name, "description": item.description })

# Ruta para actualizar un item
@items_bp.route('/<item_id>', methods=['PUT'])
def update_item(item_id):
    if not item_id.isdigit():  # Verifica si item_id es numérico
        return jsonify({"error": "The route expects a numeric ID."}), 400
    
    # Acceder a la sesión actual
    session = db.session
    
    # Usar Session.get() en lugar de Query.get()
    item = session.get(Item, item_id)
    if item is None:
        return jsonify({"error": "Item with ID  does not exist. Please try another ID.".format(item_id)}), 404

    data = request.get_json()
    item.name = data['name']
    item.description = data.get('description')
    db.session.commit()
    return jsonify({"message": "Item updated", "item": {"id": item.id, "name": item.name, "description": item.description}})

#Ruta para eliminar un Item
@items_bp.route('/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    # Si el id no es un numero
    if not item_id.isdigit():
        return jsonify({ "error": "La ruta espera un Id numerico" }), 400
    
    # Acceder a la sesión actual
    session = db.session

    #Busca el item por el id
    # Usar Session.get() en lugar de Query.get()
    item = session.get(Item, item_id)
    
    # Si no existe el Item
    if item is None:
        return jsonify({"error": "El Item con el id proporcionado no existe".format(item_id)}), 404
    
    db.session.delete(item)
    db.session.commit()
    # Retorna el mensaje de que se borro el item
    # Retorna los datos del item eliminado
    return jsonify({ "message": "Item deleted", "item": { "id": item.id, "name": item.name, "description": item.description} })

```


# Levanta el servidor de desarrollo / Firts run the developer server

```bash
cd src
```

Ejecuta el siguiente comando: 


Run the following command: 

```bash
python app.py
```

Puedes ir al `Readme.md` para ver como funciona la API.

You can go to `Readme.md` file to see how the API documentation.


# Test
Vamos a hacer test a nuestra API para asegurar que funcione correctamente.

We are going to test our API to make sure it works correctly.

## Instalar Pytest / Install Pytest

```bash
pip install pytest
```
Vamos a la carpeta test.

Go to the test folder.

El archivo `__init__.py` puedes dejarlo vacio.

The file `__init__.py` you can leave it empty.


Vamos al archivo `/test/test_items.py`

Go to the file `/test/test_items.py`

Imports necesarios:

Required imports:

```python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from src.app import app, db
from src.models.item import Item
```

Inicializar Test y Base de Datos

Initialize Test and Database

```python
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.session.remove()
        db.drop_all()
```


Test para crear nuevo Item

Test to create a new item

```python
def test_create_item(client):
    response = client.post('/items/', json={
        'name': 'Test Item',
        'description': 'This is a test item'
    })
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['message'] == 'Item Created'
```
Test para obtener todos los items


Test to get all items

```python 
def test_get_all_items(client):
    # Creamos dos items para probar la obtención de todos los items
    item1 = Item(name='Test Item 1', description='Description 1')
    item2 = Item(name='Test Item 2', description='Description 2')
    db.session.add_all([item1, item2])
    db.session.commit()

    # Realizamos la solicitud para obtener todos los items
    response = client.get('/items/')
    json_data = response.get_json()

    assert response.status_code == 200
    assert len(json_data) == 2  # Deben haber 2 items
    assert json_data[0]['name'] == 'Test Item 1'
    assert json_data[1]['name'] == 'Test Item 2'
```


Test para obtener un item por id


Test to get an item by id

```python
def test_get_item(client):
    with app.app_context():
        item = Item(name='Test Item', description='Test Description')
        db.session.add(item)
        db.session.commit()

        # Refrescamos el estado del objeto para asegurarnos de que está vinculado a la sesión
        db.session.refresh(item)

        response = client.get(f'/items/{item.id}')
        json_data = response.get_json()
        
        assert response.status_code == 200
        assert json_data['name'] == item.name
        assert json_data['description'] == item.description
```


Test para obtener un item por id - Debe devolver que el item no existe


Test to get an item by id - It's return item doesn't exist

```python 
def test_get_nonexistent_item(client):
    response = client.get('/items/999')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['error'] == 'El Item con el Id proporcionado no existe '
```

Test para actualizar un item

Test to update an item

```python
def test_update_item(client):
    with app.app_context():
        # Creamos un item para probar la actualización
        item = Item(name='Old Name', description='Old Description')
        db.session.add(item)
        db.session.commit()

        # Refrescamos el estado del objeto para asegurarnos de que está vinculado a la sesión
        db.session.refresh(item)

        # Realizamos la solicitud para actualizar el item
        response = client.put(f'/items/{item.id}', json={
            'name': 'New Name',
            'description': 'New Description'
        })
        json_data = response.get_json()

        assert response.status_code == 200
        assert json_data['message'] == 'Item updated'
        assert json_data['item']['name'] == 'New Name'
        assert json_data['item']['description'] == 'New Description'

```

Test para eliminar un item

Test to delete an item

```python
def test_delete_item(client):
    item = Item(name='Test Item', description='Test Description')
    db.session.add(item)
    db.session.commit()

    response = client.delete(f'/items/{item.id}')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Item deleted'
    assert json_data['item']['name'] == 'Test Item'
```

## Archivo `test_items.py` Completo / File `test_items.py` Completed

```python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from src.app import app, db
from src.models.item import Item

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.session.remove()
        db.drop_all()

def test_create_item(client):
    response = client.post('/items/', json={
        'name': 'Test Item',
        'description': 'This is a test item'
    })
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['message'] == 'Item Created'


def test_get_all_items(client):
    # Creamos dos items para probar la obtención de todos los items
    item1 = Item(name='Test Item 1', description='Description 1')
    item2 = Item(name='Test Item 2', description='Description 2')
    db.session.add_all([item1, item2])
    db.session.commit()

    # Realizamos la solicitud para obtener todos los items
    response = client.get('/items/')
    json_data = response.get_json()

    assert response.status_code == 200
    assert len(json_data) == 2  # Deben haber 2 items
    assert json_data[0]['name'] == 'Test Item 1'
    assert json_data[1]['name'] == 'Test Item 2'


def test_get_item(client):
    with app.app_context():
        item = Item(name='Test Item', description='Test Description')
        db.session.add(item)
        db.session.commit()

        # Refrescamos el estado del objeto para asegurarnos de que está vinculado a la sesión
        db.session.refresh(item)

        response = client.get(f'/items/{item.id}')
        json_data = response.get_json()
        
        assert response.status_code == 200
        assert json_data['name'] == item.name
        assert json_data['description'] == item.description


def test_get_nonexistent_item(client):
    response = client.get('/items/999')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['error'] == 'El Item con el Id proporcionado no existe '


def test_update_item(client):
    with app.app_context():
        # Creamos un item para probar la actualización
        item = Item(name='Old Name', description='Old Description')
        db.session.add(item)
        db.session.commit()

        # Refrescamos el estado del objeto para asegurarnos de que está vinculado a la sesión
        db.session.refresh(item)

        # Realizamos la solicitud para actualizar el item
        response = client.put(f'/items/{item.id}', json={
            'name': 'New Name',
            'description': 'New Description'
        })
        json_data = response.get_json()

        assert response.status_code == 200
        assert json_data['message'] == 'Item updated'
        assert json_data['item']['name'] == 'New Name'
        assert json_data['item']['description'] == 'New Description'

        
def test_delete_item(client):
    item = Item(name='Test Item', description='Test Description')
    db.session.add(item)
    db.session.commit()

    response = client.delete(f'/items/{item.id}')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Item deleted'
    assert json_data['item']['name'] == 'Test Item'

```

Ejecuta el siguiente comando para realizar los test:

Run the following command to perform the test:

```bash
pytest
```

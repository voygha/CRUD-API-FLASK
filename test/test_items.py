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

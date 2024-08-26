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


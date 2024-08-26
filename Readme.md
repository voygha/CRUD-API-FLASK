# CRUD API con Python y Flask

## Este proyecto es una API con funciones CRUD hechas con Python y Flask
Este proyecto nos ayudara a crear una API que permita modificar una base de Datos de SqlAlchemy.

## Ejecucion / Execute

### Clona el repositorio / Clone the Repo


### Ingresa a la carpeta `src` / Go to the `src` folder 
```bash
cd src
```
#### Levanta el servidor de desarrollo / Firts run the developer server

Ejecuta el siguiente comando: / 
Run the following command: 

```bash
python app.py
```

## Rutas de la API / API routes
Vamos a describir las funciones de los Endpoints  y como usar cada uno de ellos.


We will describe the functions of the endpoints and how to use each of them

### Crear un Item / Create a new Item
Para crear un nuevo item necesitamos pasarle 2 parametros en Content-Type: aplication/json 

To create a new item, you need to pass 2 parameters in content type Application/json :

- name
- description

Endpoint: http://127.0.0.1:5000/items/

Metodo - Method: POST

Descripcion - Description: Crea un nuevo Item - Create a new Item

Respuesta del servidor - The server responds: 

```json
{
  "item": {
    "description": "A sample item",
    "id": 5,
    "name": "Item5"
  },
  "message": "Item Created"
}
```

### Obtener todos los items / Get all Items
Para obtener todos los items unicamente necesitaremos el endpoint 

You only need the endpoint to get all items:

Endpoint: http://127.0.0.1:5000/items/

Metodo - Method: GET

Descripcion - Description: Obtiene todos los items - Get all items

Respuesta del servidor - The server responds: 

```json
[
  {
    "description": "A sample item",
    "id": 1,
    "name": "Item1"
  },
  {
    "description": "Item 2 Updated",
    "id": 2,
    "name": "Item2"
  },
  {
    "description": "A sample item",
    "id": 4,
    "name": "Item4"
  },
  {
    "description": "A sample item",
    "id": 5,
    "name": "Item5"
  }
]
```

### Obtener item por ID / Get an Item by ID
Necesitamos el Endpoint y el ID del item que queremos obtener

You need the endpoint and the item ID to you want to get:

Endpoint: http://127.0.0.1:5000/items/4 <- Reemplazalo por el ID - Replace it with the ID

Metodo - Method: GET

Descripcion - Description: Obtiene un item por ID - Get an item by ID

Respuesta del servidor - The server responds: 

```json
{
  "description": "A sample item",
  "id": 4,
  "name": "Item4"
}
```

### Actualizar un Item / Update a existing Item
Para actualizar un item necesitamos pasarle el parametro o parametros  que queremos actualizar en el Content-Type: aplication/json 


To update a existing item, you need to pass the parameter or parameters in the content type Application/json :

- name
- description

Example:
"Content-Type: application/json":
```json
{
  "name":"Item2 New",
  "description":"Item 2 Updated"
}
```

Endpoint: http://127.0.0.1:5000/items/2 <- Reemplazalo por el ID - Replace it with the ID

Metodo - Method: PUT

Descripcion - Description: Actualiza un Item existente - Update a Existing Item

Respuesta del servidor - The server responds: 

```json
{
  "item": {
    "description": "Item 2 Updated",
    "id": 2,
    "name": "Item2 New"
  },
  "message": "Item updated"
}
```


### Eliminar un item por ID / Delete an Item by ID
Necesitamos el Endpoint y el ID del item que queremos eliminar

You need the endpoint and the item ID to you want to delete:

Endpoint: http://127.0.0.1:5000/items/6 <- Reemplazalo por el ID - Replace it with the ID

Metodo - Method: DELETE

Descripcion - Description: Obtiene un item por ID - Get an item by ID

Respuesta del servidor - The server responds: 

```json
{
  "item": {
    "description": "A sample item",
    "id": 6,
    "name": "Item6"
  },
  "message": "Item deleted"
}
```

## Realizar la Aplicacion desde Cero / Build the Application step by step 

En el archivo `steps.md` podras encontrar como realizar la aplicacion pasa a paso desde cero.

In the file `steps.md` you can read how to build the aplication step by step from scrach 

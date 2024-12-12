from flask import Flask, jsonify, request
from config import Config
from game_system import GameSystem

app = Flask(__name__)
app.config.from_object(Config)
game_system = GameSystem()

@app.route('/jugadores', methods=['POST'])
def agregar_jugador():
    datos = request.json
    game_system.add_player(datos['id'], datos['username'], datos['level'], datos['score'], datos['team'])
    return jsonify({'mensaje': 'Jugador agregado'}), 201

@app.route('/jugadores/<int:id>', methods=['PUT'])
def actualizar_jugador(id):
    datos = request.json
    game_system.update_player(id, **datos)
    return jsonify({'mensaje': 'Jugador actualizado'}), 200

@app.route('/jugadores/<int:id>', methods=['DELETE'])
def eliminar_jugador(id):
    game_system.delete_player(id)
    return jsonify({'mensaje': 'Jugador eliminado'}), 200

@app.route('/jugadores/<int:id>', methods=['GET'])
def obtener_jugador(id):
    jugador = game_system.get_player(id)
    return jsonify(jugador), 200

@app.route('/inventario/<int:id>', methods=['POST'])
def agregar_item_inventario(id):
    datos = request.json
    game_system.add_item_to_inventory(id, datos['item_name'], datos['item_description'])
    return jsonify({'mensaje': 'Item agregado'}), 201

@app.route('/inventario/<int:id>', methods=['DELETE'])
def eliminar_item_inventario(id):
    datos = request.json
    game_system.remove_item_from_inventory(id, datos['item_name'])
    return jsonify({'mensaje': 'Item eliminado'}), 200

import heapq
from datetime import datetime
from models import Jugador, Mundo, Partida, Ranking, session

class GameSystem:
    def __init__(self):
        self.match_history = None  # Árbol binario para partidas

    # Gestión de jugadores
    def add_player(self, player_id, username, level, score, team):
        nuevo_jugador = Jugador(id=player_id, nombre_usuario=username, nivel=level, puntuacion=score, equipo=team, inventario={})
        session.add(nuevo_jugador)
        session.commit()

    def update_player(self, player_id, **kwargs):
        jugador = session.query(Jugador).filter_by(id=player_id).first()
        for key, value in kwargs.items():
            setattr(jugador, key, value)
        session.commit()

    def delete_player(self, player_id):
        jugador = session.query(Jugador).filter_by(id=player_id).first()
        session.delete(jugador)
        session.commit()

    def get_player(self, player_id):
        jugador = session.query(Jugador).filter_by(id=player_id).first()
        return jugador

    # Gestión de inventario
    def add_item_to_inventory(self, player_id, item_name, item_description):
        jugador = session.query(Jugador).filter_by(id=player_id).first()
        inventario = jugador.inventario
        inventario[item_name] = item_description
        jugador.inventario = inventario
        session.commit()

    def remove_item_from_inventory(self, player_id, item_name):
        jugador = session.query(Jugador).filter_by(id=player_id).first()
        inventario = jugador.inventario
        if item_name in inventario:
            del inventario[item_name]
        jugador.inventario = inventario
        session.commit()

    # Gestión de mundos virtuales (grafos)
    def create_world(self, world_id):
        nuevo_mundo = Mundo(id=world_id, grafo_serializado={})
        session.add(nuevo_mundo)
        session.commit()

    def add_connection(self, world_id, origin, destination, weight):
        mundo = session.query(Mundo).filter_by(id=world_id).first()
        grafo = mundo.grafo_serializado
        if origin not in grafo:
            grafo[origin] = []
        if destination not in grafo:
            grafo[destination] = []
        grafo[origin].append((destination, weight))
        grafo[destination].append((origin, weight))
        mundo.grafo_serializado = grafo
        session.commit()

    def find_shortest_path(self, world_id, start, end):
        mundo = session.query(Mundo).filter_by(id=world_id).first()
        grafo = mundo.grafo_serializado
        distances = {node: float('inf') for node in grafo}
        distances[start] = 0
        priority_queue = [(0, start)]
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > distances[current_node]:
                continue
            for neighbor, weight in grafo[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        return distances[end]

    # Sistema de partidas (árbol binario)
    class TreeNode:
        def __init__(self, date, match_data):
            self.date = date
            self.match_data = match_data
            self.left = None
            self.right = None

    def add_match(self, date, match_data):
        if not self.match_history:
            self.match_history = self.TreeNode(date, match_data)
        else:
            self._insert_match(self.match_history, date, match_data)

    def _insert_match(self, node, date, match_data):
        if date < node.date:
            if not node.left:
                node.left = self.TreeNode(date, match_data)
            else:
                self._insert_match(node.left, date, match_data)
        else:
            if not node.right:
                node.right = self.TreeNode(date, match_data)
            else:
                self._insert_match(node.right, date, match_data)

    def search_matches_in_range(self, start_date, end_date):
        result = []
        self._search_in_range(self.match_history, start_date, end_date, result)
        return result

    def _search_in_range(self, node, start_date, end_date, result):
        if not node:
            return
        if start_date <= node.date <= end_date:
            result.append(node.match_data)
        if node.date > start_date:
            self._search_in_range(node.left, start_date, end_date, result)
        if node.date < end_date:
            self._search_in_range(node.right, start_date, end_date, result)

    # Gestión de ranking
    def update_ranking(self, player_id, score):
        ranking = session.query(Ranking).filter_by(id_jugador=player_id).first()
        if not ranking:
            ranking = Ranking(id_jugador=player_id, puntuacion=score, posicion=0)
            session.add(ranking)
        else:
            ranking.puntuacion = score
        session.commit()

    def get_top_players(self, top_n=10):
        top_players = session.query(Ranking).order_by(Ranking.puntuacion.desc()).limit(top_n).all()
        return [(player.id_jugador, player.puntuacion) for player in top_players]

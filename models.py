from sqlalchemy import create_engine, Column, Integer, String, JSON, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Jugador(Base):
    __tablename__ = 'jugadores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False)
    nivel = Column(Integer, nullable=False)
    puntuacion = Column(Integer, nullable=False)
    equipo = Column(String(50))
    inventario = Column(JSON)

class Mundo(Base):
    __tablename__ = 'mundos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    grafo_serializado = Column(JSON)

class Partida(Base):
    __tablename__ = 'partidas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DATETIME, nullable=False)
    equipo1 = Column(String(50))
    equipo2 = Column(String(50))
    resultado = Column(String(50))

class Ranking(Base):
    __tablename__ = 'ranking'
    id_jugador = Column(Integer, primary_key=True)
    puntuacion = Column(Integer)
    posicion = Column(Integer)

engine = create_engine('mysql+pymysql://root:@localhost/videojuego')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

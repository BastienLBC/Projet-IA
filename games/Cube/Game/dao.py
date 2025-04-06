from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass 

engine = create_engine('sqlite:///store.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)  # Ajout d'une clé primaire
    chaine = Column(String)

    
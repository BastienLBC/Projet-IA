from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dico import generate_key

class Base(DeclarativeBase):
    pass

engine = create_engine('sqlite:///store.db')
# Création d'une session
Session = sessionmaker(bind=engine)
SESSION = Session()

class QTable(Base):
    __tablename__ = 'q_table'
    unique_key = Column(String, primary_key=True)
    reward = Column(Float)

    def to_dto(self):
        return {
            'unique_key': self.unique_key,
            'reward': self.reward
        }

    @classmethod
    def from_dto(cls, data: dict):
        return cls(
            unique_key=data.get('unique_key'),
            reward=data.get('reward')
        )

def init_db():
    # Création des tables
    Base.metadata.create_all(engine)

def find_all_entries():
    """
    Get all entries from the database
    @return: list of dict
    """
    entries = SESSION.query(QTable).all()
    return [entry.to_dto() for entry in entries]
    
def find_entry_by_key(unique_key):
    """
    Find an entry by unique key
    @param unique_key: str
    @return: dict
    """
    entry = SESSION.query(QTable).filter(QTable.unique_key == unique_key).first()
    return entry.to_dto() if entry else None

def save_entry(entry_dto):
    """
    Save or update an entry in the database.
    @param entry_dto: dict
    """
    # Check if the entry with the unique_key already exists
    existing_entry = SESSION.query(QTable).filter(QTable.unique_key == entry_dto['unique_key']).first()

    if existing_entry:
        # If the entry exists, update the reward value
        existing_entry.reward = entry_dto['reward']
        print(f"Updated entry with unique_key: {entry_dto['unique_key']} to reward: {entry_dto['reward']}")
    else:
        # If the entry doesn't exist, insert a new record
        new_entry = QTable.from_dto(entry_dto)
        SESSION.add(new_entry)
        print(f"Saved new entry with unique_key: {entry_dto['unique_key']} and reward: {entry_dto['reward']}")

    # Commit the transaction
    try:
        SESSION.commit()
    except Exception as e:
        SESSION.rollback()  # Rollback the transaction in case of error
        print(f"Error saving entry: {e}")
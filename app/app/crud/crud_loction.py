from sqlalchemy.orm import Session

from app import schemas
from app.models.location import State, City


class Location:

    def __init__(self):
        pass

    def get_all_states(self, db: Session):
        states = db.query(State).all()
        return [{"id": state.id, "name": state.name} for state in states]

    def get_cities_by_state(self, db: Session, params):
        state = db.query(State).filter(State.id == params.state_id).first()
        if not state:
            return []
        
        cities = db.query(City).filter(City.state_id == state.id).all()
        print(cities)
        return cities
        

crud_location = Location()
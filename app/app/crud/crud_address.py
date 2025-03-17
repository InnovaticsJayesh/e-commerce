from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.models.user import Address
from app.models.location import Country, State, City


from app.models.location import State, City, Country

class AddressInfo:

    def __init__(self):
        pass

    def create_address(self, current_user, db: Session, params):
        state = db.query(State).filter(State.id == params.state_id).first()
        if not state:
            return {'success': False, 'msg': f'State not found with ID "{params.state_id}"'}

        city = db.query(City).filter(City.id == params.city_id, City.state_id == params.state_id).first()
        if not city:
            return {'success': False, 'msg': f'City with ID "{params.city_id}" does not belong to state ID "{params.state_id}" or not found'}
        params.name = params.name.strip()
        params.address = params.address.strip()
        params.landmark = params.landmark.strip()

        if not (100000 <= params.pincode <= 999999):
            return {'success': False, 'msg': 'Invalid pincode. It must be a 6-digit number'}

        new_address = Address(
            name=params.name,
            address=params.address,
            country_id=params.country_id,
            state_id=params.state_id,
            city_id=params.city_id,
            landmark=params.landmark,
            pincode=params.pincode,
            user_id=current_user.id
        )
        
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        
        return {'success': True, 'msg': 'Address added successfully'}



    def read_address(self, current_user, db: Session):
        if not current_user:
            return {'success': False, 'msg': 'Unable to find User'}
        address_read = (db.query(Address.id, Address.name, Address.address,
                                 Address.pincode, Address.landmark,
                                 Country.name.label("country"), State.name.label("state"),
                                 City.name.label("city"), Address.created_at,
                                 Address.updated_at
                                 )
                       .join(Country, Address.country_id == Country.id)
                       .join(State, Address.state_id == State.id)
                       .join(City, Address.city_id == City.id)
                       .filter(Address.user_id == current_user.id)
                       .all()
                       )
        if not address_read:
            return {'success': False, 'msg': 'No address found'}
        addresses = [{"id": addr.id, "name": addr.name, "address": addr.address,
                      "pincode": addr.pincode, "landmark": addr.landmark,
                      "country": addr.country, "state": addr.state,
                      "city": addr.city}
            for addr in address_read
        ]
        return {'success': True, 'addresses': addresses}
    

    def read_single_address(self, address_id, current_user, db: Session):
        if not current_user:
            return {'success': False, 'msg': 'Unable to find User'}
        
        address = (db.query(Address.id, Address.name, Address.address,
                            Address.pincode, Address.landmark,
                            Country.name.label("country"), State.name.label("state"),
                            City.name.label("city"), Address.created_at, Address.updated_at)
                .join(Country, Address.country_id == Country.id)
                .join(State, Address.state_id == State.id)
                .join(City, Address.city_id == City.id)
                .filter(Address.id == address_id, Address.user_id == current_user.id)
                .first())
        
        if not address:
            return None
        
        return {
            "id": address.id,
            "name": address.name,
            "address": address.address,
            "pincode": address.pincode,
            "landmark": address.landmark,
            "country": address.country,
            "state": address.state,
            "city": address.city
        }


    def update_address(self, db: Session, current_user, address_id: int, params):
        address = db.query(Address).filter(Address.id == address_id, Address.user_id == current_user.id).first()
        if not address:
            return {"success": False, "msg": "Address not found or unauthorized"}

        params_dict = params.dict(exclude_unset=True)

        if not params_dict:
            return {"success": False, "msg": "No changes provided"}

        if "state_id" in params_dict:
            state = db.query(State).filter(State.id == params_dict["state_id"]).first()
            if not state:
                return {"success": False, "msg": f'State not found with ID "{params_dict["state_id"]}"'}

        if "city_id" in params_dict and "state_id" in params_dict:
            city = db.query(City).filter(City.id == params_dict["city_id"], City.state_id == params_dict["state_id"]).first()
            if not city:
                return {"success": False, "msg": f'City with ID "{params_dict["city_id"]}" does not belong to state ID "{params_dict["state_id"]}" or not found'}

        for key, value in params_dict.items():
            setattr(address, key, value)

        db.commit()
        db.refresh(address)

        return {"success": True, "msg": "Address updated successfully"}





    def delete_address(self, current_user, db: Session, address_id: int):
        address = db.query(Address).filter(Address.id == address_id, Address.user_id == current_user.id).first()
        if not address:
            return {'success': False, 'msg': 'Address not found'}
        db.delete(address)
        db.commit()
        return {'success': True, 'msg': 'Address deleted successfully'}


crud_address = AddressInfo()


